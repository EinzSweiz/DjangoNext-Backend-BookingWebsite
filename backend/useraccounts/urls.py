from django.urls import path
from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.views import LoginView, LogoutView, PasswordResetConfirmView, PasswordResetView
from dj_rest_auth.registration.views import RegisterView
from useraccounts import api
from .views import CustomLoginView
from .serializers import CustomRegisterSerializer
from .views import confirm_email

urlpatterns = [
    path('register/', RegisterView.as_view(serializer_class=CustomRegisterSerializer), name='rest_register'),
    path('login/', CustomLoginView.as_view(), name='rest_login'),
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    path('myreservations/', api.reservations_list, name='api_reservations_list'),
    path('<uuid:user_id>/<token>/', confirm_email, name='confirm_email'),
    path('<uuid:pk>/', api.landlord_detail, name='api_landlord_detail'),
    path('profile/<uuid:pk>/', api.profile_detail, name='profile_detail'),
    path('password/reset/', PasswordResetView.as_view(extra_context={
                'protocol': 'https',
                'domain': 'www.diplomaroad.pro',
                'site_name': 'DiplomaRoad',
            }), name='rest_password_reset'),    
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('profile/update/<uuid:pk>', api.update_profile, name='update_profile'),
]
