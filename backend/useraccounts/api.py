from .serializers import UserDetailSerializer, UserProfileUpdateSerializer, UserProfileSerializer, PasswordResetSerializer
from django.http import JsonResponse
from .models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from property.serializers import ResirvationListSerializer
import logging
from django.shortcuts import redirect
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount, SocialToken
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tasks import send_reset_email
from django.contrib.auth.tokens import default_token_generator
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
    social_account = SocialAccount.objects.get(user=user, provider='google')
    if not social_account:
        existing_user = User.objects.get(email=user.email)
        if existing_user:
            SocialAccount.objects.create(user=existing_user, provider='google')
            user = existing_user
        else:
            return JsonResponse({'message': 'No social account found and no existing user to link.'}, status=404)
    

    token = SocialToken.objects.filter(account=social_account).first()

    if token:
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        user_id = user.id
        return redirect(f'https://www.diplomaroad.pro/login/callback/?access_token={access_token}&refresh_token={refresh_token}&user_id={user_id}')   
    else:
        return JsonResponse({'message': 'No tokens found'})

@api_view(['POST'])
def validate_google_token(request):
    google_access_token = request.data.get('access_token')

    if not google_access_token:
        return JsonResponse({'detail': 'Access token is missing'}, status=400)
    
    # Assuming you have a way to validate the token and retrieve user info
    try:
        # Use the SocialAccount model to find the associated user
        social_account = SocialAccount.objects.filter(
            socialtoken__token=google_access_token
        ).first()

        if not social_account:
            return JsonResponse({'detail': 'User not found'}, status=404)

        user = social_account.user
        user_id = str(user.id)  # Get the user ID as a string

        return JsonResponse({'valid': True, 'user_id': user_id})

    except Exception as e:
        return JsonResponse({'detail': str(e)}, status=500)
    
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def password_reset(request):
    serializer = PasswordResetSerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=400)
    
    email = serializer.validated_data['email']
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({"error": "No user with this email"}, status=404)
    
    # Generate token and uid
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    
    # Build the password reset confirm URL
    reset_url = f'www.diplomaroad.pro/api/auth/password/reset/confirm/{uid}/{token}/'
    
    # Send email asynchronously using Celery
    send_reset_email.delay(email, reset_url)
    
    return JsonResponse({"message": "Password reset email sent successfully"}, status=200)
