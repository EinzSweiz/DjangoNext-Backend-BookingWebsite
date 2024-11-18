from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import Property, Reservation
from .serializers import PropertyListSerializer, PropertyDetailSerializer, ResirvationListSerializer
from .forms import PropertyForm
from useraccounts.models import User
from rest_framework_simplejwt.tokens import AccessToken

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_list(request):
    user = request.user
    favorites = []

    # Filter properties based on query parameters
    qs = Property.objects.all()
    landlord_id = request.GET.get('landlord_id')
    if landlord_id:
        qs = qs.filter(landlord_id=landlord_id)
    if request.GET.get('is_favorite'):
        qs = qs.filter(favorited=user)

    # Collect IDs of favorite properties
    if user.is_authenticated:
        favorites = qs.filter(favorited=user).values_list('id', flat=True)

    serializer = PropertyListSerializer(qs, many=True)
    return JsonResponse({
        'data': serializer.data,
        'favorites': list(favorites),
    })



@api_view(['POST', 'FILES'])
def create_property(request):
    form = PropertyForm(request.POST, request.FILES)
    if form.is_valid():
        property = form.save(commit=False)
        property.landlord = request.user
        property.save()
        return JsonResponse({'success': True})
    else:
        print('Error', form.errors, form.non_field_errors)
        return JsonResponse({'errors', form.errors.as_json()}, status=400)
    

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
    property = Property.objects.get(pk=pk)

    if request.user in property.favorited.all():
        property.favorited.remove(request.user)
        return JsonResponse({'is_favorited': False})
    else:
        property.favorited.add(request.user)
        return JsonResponse({'is_favorited': True})