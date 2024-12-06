from django.http import JsonResponse
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from .models import User
from dj_rest_auth.views import LoginView
from django.urls import reverse
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

def google_login_view(request):
    """
    Custom view to provide Google OAuth login URL for frontend.
    """
    # Use Django reverse to get the login URL
    login_url = reverse('socialaccount_login', args=['google'])
    
    # Build the full URL
    full_url = request.build_absolute_uri(login_url)
    
    # Return as JSON response
    return JsonResponse({'redirect_url': full_url})
