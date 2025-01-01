from django.urls import path
from . import api

urlpatterns = [
    path('create/', api.CreateInquiryAPIView.as_view(), name='api_create_inquiry'),
    path('get/', api.InquiriesAPIView.as_view(), name='api_inquiries_view'),
    path('get/<int:pk>/', api.GetInquiryAPIView.as_view(), name='api_detail_view'),
    path('assign-inquiry/<int:inquiry_id>/', api.AssignInquiryAPIView.as_view(), name='api_assign_inquiry'),
    path('customer-service-agents/', api.GetCustomerServiceAgentsAPIView.as_view(), name='api_customer_service_agents'),
    path('add-message/<int:pk>/', api.AddMessageAPIView.as_view(), name='api_add_message'),
    path('update-status/<int:pk>/', api.UpdateInquiryStatusAPIView.as_view(), name='api_update_status')
]