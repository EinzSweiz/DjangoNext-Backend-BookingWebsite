from django.urls import path
from . import api

urlpatterns = [
    path('all/<str:pk>', api.GetReviewsAPIView.as_view(), name='api_get_reviews'),
    path('create/<str:pk>', api.CreateReviewAPIView.as_view(), name='api_create_review'),
    path('report/create/<int:pk>/', api.CreateReviewReportAPIView.as_view(), name='api_create_report')
]