from django.urls import path
from dj_rest_auth.views import LogoutView, PasswordResetConfirmView, PasswordResetView
from dj_rest_auth.registration.views import RegisterView
from useraccounts import api
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomLoginView, confirm_email
from .serializers import CustomRegisterSerializer

urlpatterns = [
    path('register/', RegisterView.as_view(serializer_class=CustomRegisterSerializer), name='rest_register'),
    path('login/', CustomLoginView.as_view(), name='rest_login'),
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('myreservations/', api.ReservationsListView.as_view(), name='api_reservations_list'),
    path('<uuid:user_id>/<token>/', confirm_email, name='confirm_email'),
    path('<uuid:pk>/', api.LandlordDetailView.as_view(), name='api_landlord_detail'),
    path('profile/<uuid:pk>/', api.ProfileDetailView.as_view(), name='profile_detail'),
    path('password/reset/', api.CustomPasswordResetView.as_view(), name='password_reset'),    
    path('password/reset/confirm/<uidb64>/<token>/', api.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('profile/update/<uuid:pk>', api.UpdateProfileView.as_view(), name='update_profile'),
]
