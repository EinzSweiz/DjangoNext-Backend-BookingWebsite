from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import Property, Reservation
from .serializers import PropertyListSerializer, PropertyDetailSerializer, ResirvationListSerializer
from .forms import PropertyForm
from django.shortcuts import get_object_or_404
from useraccounts.models import User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_list(request):
    user = None
    try:
        print("Extracting token from Authorization header...")
        # Extract token from Authorization header
        token = request.META['HTTP_AUTHORIZATION'].split('Bearer ')[1]
        print(f"Token extracted: {token}")
        
        token = AccessToken(token)
        print(f"Token decoded: {token}")

        # Extract user ID from token payload
        user_id = token.payload.get('user_id')
        print(f"User ID extracted: {user_id}")

        if user_id is None:
            raise AuthenticationFailed('User ID not found in token')
        
        user = User.objects.get(pk=user_id)
        print(f"User found: {user}")
    except KeyError as e:
        print(f"KeyError: {str(e)} - Authorization token not provided")
        raise AuthenticationFailed('Authorization token not provided')
    except (AuthenticationFailed, User.DoesNotExist) as e:
        print(f"Exception occurred: {str(e)}")
        user = None

    favorites = []
    country = request.GET.get('country', '')
    category = request.GET.get('category', '')
    checkin_date = request.GET.get('checkIn', '')
    checkout_date = request.GET.get('checkOut', '')
    bedrooms = request.GET.get('numBedrooms', '')
    bathrooms = request.GET.get('numBathrooms', '')
    guests = request.GET.get('numGuests', '')
    is_favorites = request.GET.get('is_favorites', '')

    print(f"Query parameters - country: {country}, category: {category}, checkIn: {checkin_date}, checkOut: {checkout_date}")
    print(f"bedrooms: {bedrooms}, bathrooms: {bathrooms}, guests: {guests}, is_favorites: {is_favorites}")

    # Filter properties based on query parameters
    qs = Property.objects.all()
    landlord_id = request.GET.get('landlord_id')
    print(f"Filtering by landlord_id: {landlord_id}")
    
    if landlord_id:
        qs = qs.filter(landlord_id=landlord_id)
        print(f"Properties filtered by landlord_id: {qs}")

    if is_favorites and user:
        print(f"Filtering by favorites for user: {user}")
        qs = qs.filter(favorited__in=[user])
        print(f"Properties after filtering by favorites: {qs}")

    if checkin_date and checkout_date:
        print(f"Filtering by checkin and checkout dates: {checkin_date} to {checkout_date}")
        exact_matches = Reservation.objects.filter(start_date=checkin_date) | Reservation.objects.filter(end_date=checkout_date)
        overlap_matches = Reservation.objects.filter(start_date__lte=checkout_date, end_date__gte=checkin_date)
        all_matches = []
        for reservation in exact_matches | overlap_matches:
            all_matches.append(reservation.property_id)
        print(f"Reservations that match dates: {all_matches}")
        qs = qs.exclude(id__in=all_matches)
        print(f"Properties after excluding overlapping reservations: {qs}")

    # Collect IDs of favorite properties
    if user and user.is_authenticated:
        print(f"Collecting favorite properties for user {user}")
        favorites = qs.filter(favorited=request.user).values_list('id', flat=True)
        print(f"Favorite properties IDs: {favorites}")

    if guests:
        print(f"Filtering by guests: {guests}")
        qs = qs.filter(guests__gte=guests)
        print(f"Properties after filtering by guests: {qs}")

    if bedrooms:
        print(f"Filtering by bedrooms: {bedrooms}")
        qs = qs.filter(bedrooms__gte=bedrooms)
        print(f"Properties after filtering by bedrooms: {qs}")

    if bathrooms:
        print(f"Filtering by bathrooms: {bathrooms}")
        qs = qs.filter(bathrooms__gte=bathrooms)
        print(f"Properties after filtering by bathrooms: {qs}")

    if country:
        print(f"Filtering by country: {country}")
        qs = qs.filter(country=country)
        print(f"Properties after filtering by country: {qs}")

    if category and category != 'undefined':
        print(f"Filtering by category: {category}")
        qs = qs.filter(category=category)
        print(f"Properties after filtering by category: {qs}")

    print(f"Total properties after all filters: {qs.count()}")

    # Serialize the queryset
    serializer = PropertyListSerializer(qs, many=True)
    response_data = {
        'data': serializer.data,
        'favorites': list(favorites),
    }
    print(f"Response data: {response_data}")
    return JsonResponse(response_data)



@api_view(['POST', 'FILES'])
def create_property(request):
    try:
        print("Received new property creation request")
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.landlord = request.user
            property.save()
            return JsonResponse({'success': True})
        else:
            print('Error', form.errors, form.non_field_errors)
            return JsonResponse({'errors', form.errors.as_json()}, status=400)
    except Exception as e:
        print(f"Error: {e}")
    

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_detail(request, pk):
    object = Property.objects.get(id=pk)
    serializer = PropertyDetailSerializer(object, many=False)
    return JsonResponse(
        serializer.data
    )

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

@api_view(['POST'])
def book_property(request, pk):
    try:
        # Accessing data from the request in DRF
        start_date = request.data.get('start_date', '')
        end_date = request.data.get('end_date', '')
        total_price = request.data.get('total_price', '')
        number_of_nights = request.data.get('number_of_nights', '')
        guests = request.data.get('guests', '')
        
        # Retrieve the property and create a reservation
        property = Property.objects.get(pk=pk)

        Reservation.objects.create(
            property=property,
            start_date=start_date,
            end_date=end_date,
            number_of_nights=number_of_nights,
            total_price=total_price,
            guests=guests,
            created_by=request.user
        )
        return JsonResponse({'success': True})

    except Exception as e:
        print('Error', e)
        return JsonResponse({'success': False}, status=400)


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
    