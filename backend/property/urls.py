from django.urls import path
from . import api

urlpatterns = [
    path('properities/', api.properties_list, name='api_properties_list'),
    path('properties/create/', api.create_property, name='api_create'),
    path('properties/<uuid:pk>/', api.properties_derail, name='api_properties_detail')
]