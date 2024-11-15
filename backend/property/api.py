from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import Property
from .serializers import PropertyListSerializer, PropertyDetailSerializer
from .forms import PropertyForm

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_list(request):
    qs = Property.objects.all()
    serializer = PropertyListSerializer(qs, many=True)
    return JsonResponse({
        'data': serializer.data
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
def properties_derail(request, pk):
    object = Property.objects.get(id=pk)
    serializer = PropertyDetailSerializer(object, many=False)
    return JsonResponse(
        serializer.data
    )