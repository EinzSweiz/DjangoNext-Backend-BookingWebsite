from .serializers import UserDetailSerializer, UserProfileUpdateSerializer, UserProfileSerializer
from django.http import JsonResponse, HttpResponseRedirect
from .models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from property.serializers import ResirvationListSerializer
import logging
from django.conf import settings
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt

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

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def profile_detail(request, pk):
    logger.debug("profile_detail function called")
    try:
        logger.debug(f"Looking for user with pk={pk}")
        user = User.objects.get(pk=pk)
        # Clean problematic fields
        print(user.email)

        # Now serialize the data
        serializer = UserProfileSerializer(user)
        logger.debug(f"Serialized data: {serializer.data}")
        return JsonResponse(serializer.data)

    except User.DoesNotExist:
        logger.error(f"User with pk={pk} does not exist")
        return JsonResponse({"error": "User not found"}, status=404)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return JsonResponse({"error": "Internal server error"}, status=500)

        

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

class GoogleLoginCallbackAPI(APIView):
    permission_classes = [AllowAny]  # Allow any user to access this endpoint

    @csrf_exempt  # Disable CSRF for this view
    def get(self, request, *args, **kwargs):
        # Get the token from the URL
        token = request.GET.get('access_token', None)

        if token is None:
            return JsonResponse({'error': 'Access token not found in the request'}, status=400)

        try:
            # Decode the token
            access_token = AccessToken(token)
            user = access_token.payload.get('user_id')

            if user is None:
                return JsonResponse({'error': 'User not found in token payload'}, status=400)

            user_instance = User.objects.get(id=user)

            refresh = RefreshToken.for_user(user_instance)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            frontend_url = f"{settings.FRONTEND_URL}/auth/callback/{access_token}/{refresh_token}/{user_instance.id}/"
            return HttpResponseRedirect(frontend_url)

        except Exception as e:
            return JsonResponse({'error': f'Error processing the token: {str(e)}'}, status=400)