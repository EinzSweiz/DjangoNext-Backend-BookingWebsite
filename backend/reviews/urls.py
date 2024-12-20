from django.urls import path
from . import api

urlpatterns = [
    path('all/', api.get_reviews_api, name='api_get_reviews'),
    path('create/', api.create_reviews_api, name='api_create_review'),
]