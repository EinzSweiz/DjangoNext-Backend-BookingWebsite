from django.http import JsonResponse
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from .models import User
from dj_rest_auth.views import LoginView
from rest_framework.exceptions import AuthenticationFailed


def confirm_email(request, uidb64, token):
    try:
        # Decode the UID
        user_id = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=user_id)
        
        # Validate the token
        if default_token_generator.check_token(user, token):
            user.is_active = True  # Activate the user
            user.is_verified = True
            user.save()
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
