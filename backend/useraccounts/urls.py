from django.urls import path
from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.views import LoginView, LogoutView, PasswordResetConfirmView, PasswordResetView
from dj_rest_auth.registration.views import RegisterView
from rest_framework_simplejwt.views import TokenVerifyView
from useraccounts import api
from .api import GoogleLoginCallbackAPI
from .views import CustomLoginView
from .serializers import CustomRegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import confirm_email

urlpatterns = [
    path('register/', RegisterView.as_view(serializer_class=CustomRegisterSerializer), name='rest_register'),
    path('login/', CustomLoginView.as_view(), name='rest_login'),
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    path('token/refresh/', get_refresh_view().as_view(), name='token_refresh'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtaion'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('myreservations/', api.reservations_list, name='api_reservations_list'),
    path('<uuid:user_id>/<token>/', confirm_email, name='confirm_email'),
    path('<uuid:pk>/', api.landlord_detail, name='api_landlord_detail'),
    path('google/redirect/', GoogleLoginCallbackAPI.as_view(), name='google-callback'),
    path('profile/<uuid:pk>/', api.profile_detail, name='profile_detail'),
    path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),    
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('profile/update/<uuid:pk>', api.update_profile, name='update_profile'),
]
