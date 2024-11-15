from django.urls import path
from . import api

urlpatterns = [
    path('properities/', api.properties_list, name='api_properties_list'),
    path('properties/create/', api.create_property, name='api_create')
]