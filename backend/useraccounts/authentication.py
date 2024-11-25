from rest_framework_simplejwt.authentication import JWTAuthentication


class CookiesJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get('access_token')

        if not access_token:
            return None
        
        validate_token = self.get_validated_token(access_token)

        try:
            user = self.get_user(validate_token)
        except:
            return None
        return (user, validate_token)