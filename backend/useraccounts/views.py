from django.http import JsonResponse
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from .models import User
from dj_rest_auth.views import LoginView
from django.urls import reverse
from dj_rest_auth.views import PasswordResetView
from django.conf import settings
from allauth.account.models import EmailAddress
from rest_framework.exceptions import AuthenticationFailed


def confirm_email(request, user_id, token):
    try:
        user = User.objects.get(pk=user_id)
        
        # Validate the token
        if default_token_generator.check_token(user, token):
            user.is_active = True  # Activate the user
            user.is_verified = True
            user.save()

            email = EmailAddress.objects.get(user=user)
            email.verified = True
            email.save()
            return JsonResponse({"message": "Email confirmed successfully"}, status=200)
        else:
            return JsonResponse({"error": "Invalid or expired token"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
class CustomLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = self.user
        
        if not user.is_verified:
            raise AuthenticationFailed("E-mail is not verified.")
        
        return response


class CustomPasswordResetView(PasswordResetView):
    def get_email_context(self, *args, **kwargs):
        context = super().get_email_context(*args, **kwargs)
        
        # Get the generated reset URL by default
        reset_url = context['reset_url']
        
        # Customize the reset URL if needed
        # For example, you can prepend your custom domain
        custom_reset_url = f"https://api.diplomaroad.pro/password/reset/confirm/{reset_url.split('/')[-2]}/{reset_url.split('/')[-1]}"
        
        # Add the custom reset URL to the context
        context['reset_url'] = custom_reset_url
        
        return context
    

class CustomPasswordResetView(PasswordResetView):
    def get_email_context(self, *args, **kwargs):
        context = super().get_email_context(*args, **kwargs)
        
        # Get the generated reset URL by default
        reset_url = context['reset_url']
        
        # Customize the reset URL if needed
        # For example, you can prepend your custom domain
        custom_reset_url = f"https://www.diplomaroad.pro/password/reset/confirm/{reset_url.split('/')[-2]}/{reset_url.split('/')[-1]}"
        
        # Add the custom reset URL to the context
        context['reset_url'] = custom_reset_url
        
        return context