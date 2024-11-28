from django.urls import path
from . import api

urlpatterns = [
    path('create/', api.create_inquiry, name='api_create_inquiry'),
    path('get', api.inquiries_view, name='api_inquiries_view'),
]