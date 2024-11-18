from django.urls import path
from . import api

urlpatterns = [
    path('properities/', api.properties_list, name='api_properties_list'),
    path('properties/create/', api.create_property, name='api_create'),
    path('properties/<uuid:pk>/', api.properties_detail, name='api_properties_detail'),
    path('properties/<uuid:pk>/book/', api.book_property, name='api_properties_book'),
    path('properties/<uuid:pk>/toggle_favorite/', api.toggle_favorite, name='api_toggle_favorite'),
    path('properties/<uuid:pk>/reservations/', api.properties_reservations, name='api_properties_reservations')
]