from .serializers import UserDetailSerializer, UserProfileUpdateSerializer, UserProfileSerializer
from django.http import JsonResponse
from .models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from property.serializers import ResirvationListSerializer
import logging
from django.http import HttpResponseBadRequest
import uuid

logger = logging.getLogger(__name__)
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

def profile_detail(request, pk):
    try:
        uuid_obj = uuid.UUID(pk)  # Validate UUID format
        user = User.objects.get(pk=uuid_obj)
        print(f"User details: {vars(user)}", flush=True)
        serializer = UserProfileSerializer(user)
        return JsonResponse(serializer.data)
    except ValueError:
        return HttpResponseBadRequest("Invalid UUID format")
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    except UnicodeDecodeError as e:
        return JsonResponse({"error": f"Encoding error: {e}"}, status=400)


@api_view(['PUT'])
@authentication_classes([])
@permission_classes([])
def update_profile(request, pk):
    user = User.objects.get(pk=pk)
    serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data)
    else:
    # Log the serializer errors to check the exact issue
        print(serializer.errors)
        return JsonResponse(serializer.errors, status=400)
