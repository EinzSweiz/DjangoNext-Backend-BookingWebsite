from django.urls import path
from . import api

urlpatterns = [
    path('create/', api.create_inquiry, name='api_create_inquiry'),
    path('get/', api.inquiries_view, name='api_inquiries_view'),
    path('get/<int:pk>/', api.get_inquiry, name='api_detail_view'),
    path('assign-inquiry/<int:inquiry_id>/', api.assign_inquiry, name='api_assign_inquiry'),
    path('customer-service-agents/', api.get_customer_service_agents, name='api_customer_service_agents'),
    path('add-message/<int:pk>/', api.add_message, name='api_add_message'),
    path('update-status/<int:pk>/', api.update_inquiry_status, name='api_update_status')
]