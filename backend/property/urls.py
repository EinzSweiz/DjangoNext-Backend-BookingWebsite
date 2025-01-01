from django.urls import path
from . import api

urlpatterns = [
    path('properties/', api.PropertiesListAPIView.as_view(), name='api_properties_list'),
    path('properties/create/', api.CreatePropertyAPIView.as_view(), name='api_create'),
    path('properties/<uuid:pk>/', api.PropertyDetailAPIView.as_view(), name='api_properties_detail'),
    path('properties/<uuid:pk>/book/', api.BookPropertyAPIView.as_view(), name='api_properties_book'),
    path('properties/<uuid:pk>/toggle_favorite/', api.ToggleFavoriteAPIView.as_view(), name='api_toggle_favorite'),
    path('properties/<uuid:pk>/reservations/', api.PropertiesReservationsAPIView.as_view(), name='api_properties_reservations')
]