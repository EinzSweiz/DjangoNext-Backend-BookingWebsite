from .serializers import UserDetailSerializer, UserProfileUpdateSerializer, UserProfileSerializer
from django.http import JsonResponse
from .models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from property.serializers import ResirvationListSerializer

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def landlord_detail(request, pk):
    user = User.objects.get(pk=pk)
    serializer = UserDetailSerializer(user, many=False)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def reservations_list(request):
    qs = request.user.reservations.all()
    serializer = ResirvationListSerializer(qs, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def profile_detail(request, pk):
    user = User.objects.get(pk=pk)
    serializer = UserProfileSerializer(user)
    return JsonResponse(serializer.data)


@api_view(['PUT'])
@authentication_classes([])
@permission_classes([])
def update_profile(request):
    user = request.user
    serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=400)
