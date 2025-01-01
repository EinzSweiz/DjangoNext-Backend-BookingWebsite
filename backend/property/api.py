from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.views import APIView
from .models import Property, Reservation, PropertyImage
from .serializers import PropertyModelDynamicSerializer, ReservationListSerializer
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
from .swagger_usecases import (property_detail_schema, property_list_schema, booking_request_schema, 
                            reservation_list_schema, favorite_toggle_response_schema, create_property_request_schema)
import logging

logger = logging.getLogger('default')

stripe.api_key = settings.STRIPE_SECRET_KEY

class PropertiesListAPIView(ListAPIView):
    serializer_class = PropertyModelDynamicSerializer
    permission_classes = []
    authentication_classes = []

    @swagger_auto_schema(
        operation_summary="List all properties",
        operation_description="Retrieve a list of properties with optional filters (e.g., country, category, etc.).",
        responses={200: property_list_schema},
    )
    def get(self, request, *args, **kwargs):
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
        serializer = PropertyModelDynamicSerializer(qs, fields=['id', 'title', 'price_per_night', 'image_url','country'], many=True)
        response_data = {
            'data': serializer.data,
            'favorites': list(favorites),
            'count': qs.count(),
        }
        cache.set(cache_key, response_data, timeout=600)
        return JsonResponse(response_data)



class CreatePropertyAPIView(APIView):
    """
    Landlord can create a new property by providing necessary details.
    """

    @swagger_auto_schema(
        operation_summary="Create a property",
        operation_description="Landlord can create a new property by providing necessary details.",
        request_body=create_property_request_schema,
        responses={201: "Property successfully created"},
    )
    def post(self, request, *args, **kwargs):
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
                property_data['image'] = property_instance.image.url if property_instance.image else None

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

class PropertyDetailAPIView(RetrieveAPIView):
    permission_classes = []
    authentication_classes = []
    queryset = Property.objects.prefetch_related('extra_images')
    serializer_class = PropertyModelDynamicSerializer
    lookup_field = 'pk'

    @swagger_auto_schema(
    operation_summary="Property details",
    operation_description="Retrieve the details of a specific property.",
    responses={200: property_detail_schema, 404: "Property not found"},
    )
    def retrieve(self, request, *args, **kwargs):
        cache_key = f"property_detail_{kwargs['pk']}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return JsonResponse(cached_data, safe=False)

        instance = self.get_object()
        serializer = self.get_serializer(instance, fields=[
            'id', 'title', 'description', 'price_per_night', 'image_url',
            'bedrooms', 'bathrooms', 'guests', 'landlord', 'extra_images'
        ])
        cache.set(cache_key, serializer.data, timeout=3600)
        return JsonResponse(serializer.data, safe=False)


class PropertiesReservationsAPIView(RetrieveAPIView):
    serializer_class = ReservationListSerializer
    queryset = Property.objects.prefetch_related('reservations')
    permission_classes = []
    authentication_classes = []

    @swagger_auto_schema(
        operation_summary="List reservations for a property",
        operation_description="Retrieve all reservations for a specific property.",
        responses={200: reservation_list_schema},
    )
    def get(self, request, pk, *args, **kwargs):
        property = self.get_object()
        reservations = property.reservations.all()
        serializer = self.get_serializer(reservations, many=True)
        return JsonResponse(serializer.data, safe=False)

class BookPropertyAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Book a property",
        operation_description="Book a property by providing booking details such as start and end dates, total price, etc.",
        request_body=booking_request_schema,
        responses={200: "Booking URL returned for payment"},
    )
    def post(self, request, pk, *args, **kwargs):
        try:
            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')
            total_price = request.data.get('total_price')
            number_of_nights = request.data.get('number_of_nights')
            guests = request.data.get('guests')
            has_paid = request.data.get('has_paid', False)

            property = get_object_or_404(Property, pk=pk)
            checkout_session = product_checkout_view(request, property, pk, total_price, start_date, end_date, number_of_nights, guests, has_paid)
            return JsonResponse({'url': checkout_session.url})
        except Exception as e:
            logger.error(f"Error: {e}")
            return JsonResponse({'success': False, 'error': str(e)}, status=400)


class ToggleFavoriteAPIView(APIView):
    @swagger_auto_schema(
    operation_summary="Toggle property favorite status",
    operation_description="Toggle the favorite status of a property for the authenticated user.",
    responses={200: favorite_toggle_response_schema, 401: "Authentication required"},
    )
    def post(self, request, pk, *args, **kwargs):
        property = get_object_or_404(Property, pk=pk)

        if request.user in property.favorited.all():
            property.favorited.remove(request.user)
            return JsonResponse({'is_favorited': False})
        else:
            property.favorited.add(request.user)
            return JsonResponse({'is_favorited': True})