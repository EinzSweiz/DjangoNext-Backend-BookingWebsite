from .serializers import UserDetailSerializer, UserProfileUpdateSerializer, UserProfileSerializer, PasswordResetSerializer, SetPasswordSerializer
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
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.permissions import AllowAny
from .tasks import send_reset_email
from rest_framework.views import APIView
from django.contrib.auth.tokens import PasswordResetTokenGenerator
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
        logger.debug(user.email)

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
        logger.error(serializer.errors)
        return JsonResponse(serializer.errors, status=400)


@login_required
def google_login_callback(request):
    user = request.user

    # Attempt to fetch or create the SocialAccount
    social_account, created = SocialAccount.objects.get_or_create(
        user=user,
        provider='google',
        defaults={"uid": user.email}  # Use email as a default UID
    )

    if created:
        logger.debug("SocialAccount was created for user:", user.email)
    else:
        logger.debug("SocialAccount already exists for user:", user.email)

    # Check for a SocialToken associated with the SocialAccount
    token = SocialToken.objects.filter(account=social_account).first()

    if token:
        # Generate JWT tokens for the user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        user_id = user.id

        # Redirect with tokens
        return redirect(
            f'https://www.diplomaroad.pro/login/callback/?access_token={access_token}&refresh_token={refresh_token}&user_id={user_id}'
        )
    else:
        return JsonResponse({'message': 'No tokens found for this social account'}, status=404)

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
    
class CustomPasswordResetView(APIView):
    authentication_classes = []  # No authentication required
    permission_classes = [AllowAny]  # Allows any user to access this endpoint

    def post(self, request):
        # Validate the request data
        serializer = PasswordResetSerializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({"error": "No user with this email"}, status=404)

        # Generate UID and Token
        uid = urlsafe_base64_encode(force_bytes(user.pk))  # Generate UID
        token = PasswordResetTokenGenerator().make_token(user)  # Generate Token

        # Build the reset URL with https://
        reset_url = f'https://www.diplomaroad.pro/api/auth/password/reset/confirm/{uid}/{token}/'

        # Send the email with the reset URL using Celery (asynchronous task)
        send_reset_email.delay(email, reset_url)

        return JsonResponse({"message": "Password reset email sent successfully"}, status=200)



class CustomPasswordResetConfirmView(APIView):
    """
    Custom password reset confirm view to handle password reset functionality.
    """
    authentication_classes = []  # No authentication required
    permission_classes = [AllowAny]  # Allows any user to access this endpoint
    def post(self, request, uidb64, token):
        try:
            # Decode the UID to get the user ID
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, User.DoesNotExist):
            return JsonResponse({"error": "Invalid token or UID."}, status=400)

        # Check if the token is valid
        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            return JsonResponse({"error": "Invalid token."}, status=400)

        # Now validate the new password
        serializer = SetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            # Set the new password
            user.set_password(serializer.validated_data["new_password1"])
            user.save()
            return JsonResponse({"message": "Password has been reset successfully."}, status=200)
        
        return JsonResponse(serializer.errors, status=400)
