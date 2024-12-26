from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import Property, Reservation, PropertyImage
from .serializers import PropertyListSerializer, PropertyDetailSerializer, ResirvationListSerializer, BookingSerializer
from .forms import PropertyForm
from django.shortcuts import get_object_or_404
from useraccounts.models import User
from rest_framework.exceptions import AuthenticationFailed
from .tasks import send_property_creation_message
from django.forms.models import model_to_dict
import stripe
from my_stripe.views import product_checkout_view
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .swagger_usecases import property_detail_schema, property_list_schema, booking_request_schema, reservation_list_schema, favorite_toggle_response_schema
import logging

logger = logging.getLogger('default')

stripe.api_key = settings.STRIPE_SECRET_KEY

@swagger_auto_schema(
    method='get',
    operation_summary="List all properties",
    operation_description="Retrieve a list of properties with optional filters (e.g., country, category, etc.).",
    responses={200: property_list_schema},
)
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_list(request):
    user = None
    try:
        # Extract token from Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            raise AuthenticationFailed('Authorization token not provided')

        token = auth_header.split('Bearer ')[1]
        token = AccessToken(token)

        # Debugging the payload

        # Extract user ID from token payload
        user_id = token.payload.get('user_id')
        logger.debug('User_id:', user_id)
        if user_id is None:
            raise AuthenticationFailed('User ID not found in token')
        
        user = User.objects.get(pk=user_id)
    except KeyError:
        raise AuthenticationFailed('Authorization token not provided')
    except (AuthenticationFailed, User.DoesNotExist):
        user = None

    cache_key = f"properties_list_{request.GET.urlencode()}_{user.id if user else 'anonymous'}"
    cached_response = cache.get(cache_key)  
    logger.info(f"Cache Key: {cache_key}")
    logger.info('Cache Miss')
    favorites = []
    country = request.GET.get('country', '')
    category = request.GET.get('category', '')
    checkin_date = request.GET.get('checkIn', '')
    checkout_date = request.GET.get('checkOut', '')
    bedrooms = request.GET.get('numBedrooms', '')
    bathrooms = request.GET.get('numBathrooms', '')
    guests = request.GET.get('numGuests', '')
    is_favorites = request.GET.get('is_favorites', '')

    # Filter properties based on query parameters
    qs = Property.objects.all()
    landlord_id = request.GET.get('landlord_id')
    if landlord_id:
        qs = qs.filter(landlord_id=landlord_id)
    if is_favorites:
        if user:
            # Filter properties that are favorited by the authenticated user
            qs = qs.filter(favorited=user)
        else:
            # If the user is not authenticated, return an empty queryset
            qs = qs.none()
    if checkin_date and checkout_date:
        exact_matches = Reservation.objects.filter(start_date=checkin_date) | Reservation.objects.filter(end_date=checkout_date)
        overlap_matches = Reservation.objects.filter(start_date__lte=checkout_date, end_date__gte=checkin_date)
        all_matches = []
        for reservation in exact_matches | overlap_matches:
            all_matches.append(reservation.property_id)
        qs = qs.exclude(id__in=all_matches)

    if cached_response:
        cached_count = cached_response.get('count', 0)
        if cached_count== qs.count():
            logger.info(f"Cache hit: Returning cached response for key {cache_key}")
            return JsonResponse(cached_response)
        else:
            logger.info("Cache invalid: Length mismatch. Continuing without cached data.")
    
    # Collect IDs of favorite properties
    if user:
        favorites = Property.objects.filter(favorited=user).values_list('id', flat=True)
    else:
        favorites = []
    if guests:
        qs = qs.filter(guests__gte=guests)
    if bedrooms:
        qs = qs.filter(bedrooms__gte=bedrooms)
    if bathrooms:
        qs = qs.filter(bathrooms__gte=bathrooms)
    if country:
        qs = qs.filter(country=country)
    if category and category != 'undefined':
        qs = qs.filter(category=category)
    
    logger.debug(f"Favorites: {favorites}")

    logger.debug(
        f"Properties list API accessed. User: {user.id if user else 'Anonymous'}, "
        f"Country: {country}, Guests: {guests}, Check-in: {checkin_date}, Check-out: {checkout_date}"
    )
    serializer = PropertyListSerializer(qs, many=True)
    response_data = {
        'data': serializer.data,
        'favorites': list(favorites),
        'count': qs.count(),
    }
    cache.set(cache_key, response_data, timeout=600)
    return JsonResponse(response_data)


from django.forms.models import model_to_dict

@swagger_auto_schema(
    method='post',
    operation_summary="Create a property",
    operation_description="Landlord can create a new property by providing necessary details.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "title": openapi.Schema(type=openapi.TYPE_STRING, description="Property title"),
            "description": openapi.Schema(type=openapi.TYPE_STRING, description="Property description"),
            "price_per_night": openapi.Schema(type=openapi.TYPE_INTEGER, description="Price per night"),
            "bedrooms": openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of bedrooms"),
            "bathrooms": openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of bathrooms"),
            "guests": openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of guests"),
            "country": openapi.Schema(type=openapi.TYPE_STRING, description="Country"),
            "category": openapi.Schema(type=openapi.TYPE_STRING, description="Category"),
            "image": openapi.Schema(type=openapi.TYPE_STRING, format="binary", description="Main property image"),
        },
        required=["title", "description", "price_per_night", "bedrooms", "bathrooms", "guests", "country"],
    ),
    responses={201: "Property successfully created"},
)
@api_view(['POST'])
def create_property(request):
    try:
        logger.debug("Received new property creation request")
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_instance = form.save(commit=False)
            property_instance.landlord = request.user

            # Save the property instance
            property_instance.save()

            # Handle extra images
            extra_images = request.FILES.getlist('extra_images')
            for image in extra_images:
                PropertyImage.objects.create(property=property_instance, image=image)

            # Serialize the property data
            property_data = model_to_dict(property_instance)
            property_data['id'] = property_instance.id

            # Handle the image field manually
            if property_instance.image:
                property_data['image'] = property_instance.image.url
            else:
                property_data['image'] = None

            # Include extra images in the response
            property_data['extra_images'] = [
                {
                    'image_url': img.image.url,
                    'alt_text': img.alt_text
                } for img in property_instance.extra_images.all()
            ]

            # Pass serialized data to the message sender
            property_data['landlord_email'] = request.user.email
            property_data['landlord_name'] = request.user.name
            send_property_creation_message.delay(property_data)

            return JsonResponse({'success': True, 'property': property_data})
        else:
            logger.error(f"Form errors: {form.errors.as_json()}")
            return JsonResponse({'errors': form.errors.as_json()}, status=400)
    except Exception as e:
        logger.error(f"Error: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@swagger_auto_schema(
    method='get',
    operation_summary="Property details",
    operation_description="Retrieve the details of a specific property.",
    responses={200: property_detail_schema, 404: "Property not found"},
)
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_detail(request, pk):
    cache_key = f"property_detail_{pk}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return JsonResponse(cached_data, safe=False)
    try:
        property_object = Property.objects.prefetch_related('extra_images').get(id=pk)
        serializer = PropertyDetailSerializer(property_object, many=False)
        cache.set(cache_key, serializer.data, timeout=3600)
        return JsonResponse(
            serializer.data,
            safe=False
        )
    except Property.DoesNotExist:
        return JsonResponse({"error": "Property not found"}, status=404)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_reservations(request, pk):
    property = Property.objects.get(pk=pk)
    reservations = property.reservations.all()
    serializer = ResirvationListSerializer(reservations, many=True)
    return JsonResponse(
        serializer.data,
        safe=False
    )

@swagger_auto_schema(
    method='post',
    operation_summary="Book a property",
    operation_description="Book a property by providing booking details such as start and end dates, total price, etc.",
    request_body=booking_request_schema,
    responses={200: "Booking URL returned for payment"},
)
@api_view(['POST'])
def book_property(request, pk):
    try:
        # Accessing data from the request
        start_date = request.data.get('start_date', '')
        end_date = request.data.get('end_date', '')
        total_price = request.data.get('total_price', '')
        number_of_nights = request.data.get('number_of_nights', '')
        guests = request.data.get('guests', '')
        has_paid = request.data.get('has_paid', False)

        # Retrieve the property
        property = Property.objects.get(pk=pk)

        # Create Stripe Checkout session
        
        checkout_session = product_checkout_view(request, property, pk, total_price, start_date, end_date, number_of_nights, guests, has_paid)
        # Return the checkout session URL to redirect the user
        return JsonResponse({'url': checkout_session.url})

    except Exception as e:
        logger.error('Error:', e)
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@swagger_auto_schema(
    method='get',
    operation_summary="Toggle property favorite status",
    operation_description="Toggle the favorite status of a property for the authenticated user.",
    responses={200: favorite_toggle_response_schema, 401: "Authentication required"},
)
@api_view(['POST'])
def toggle_favorite(request, pk):

    if not request.user.is_authenticated:
        return JsonResponse({'detail': 'Authentication required.'}, status=401)
    
    property = get_object_or_404(Property, pk=pk)

    if request.user in property.favorited.all():
        property.favorited.remove(request.user)
        return JsonResponse({'is_favorited': False})
    else:
        property.favorited.add(request.user)
        return JsonResponse({'is_favorited': True})
    