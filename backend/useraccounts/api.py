from .serializers import UserDetailSerializer, UserProfileUpdateSerializer, UserProfileSerializer
from django.http import JsonResponse, HttpResponseRedirect
from .models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from property.serializers import ResirvationListSerializer
import logging
from django.shortcuts import redirect
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount, SocialToken
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
import json

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

@login_required
def google_login_callback(request):
    user = request.user
    social_accounts = SocialAccount.objects.filter(user=user)
    social_account = social_accounts.first()
    if not social_accounts:
        return JsonResponse('No user found')
    

    token = SocialToken.objects.filter(account=social_account, account_providers='google').first()

    if token:
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return redirect(f'https://www.diplomaroad.pro/login/callback/?access_token={access_token}')
    else:
        return JsonResponse('No tokens found')
    
@csrf_exempt
def validate_google_token(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            google_access_token = data.get('access_token')
            
            if not google_access_token:
                return JsonResponse({'detail': 'Access token is missing'}, status=400)
            return JsonResponse({'valid': True})
        except json.JSONDecodeError:
            return JsonResponse({'detail': 'Invalid Json'}, status=400)
    return JsonResponse({'detail': 'Method not allowed'}, status=405)