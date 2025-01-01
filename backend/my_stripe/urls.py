from django.urls import path
from . import api
urlpatterns = [
    path('payment/success/', api.PaymentSuccessAPIView.as_view(), name='api_payment_success'),
    path('payment/cancel/', api.PaymentCancelAPIView.as_view(), name='api_payment_cancel'),
    path('stripe_webhook/', api.stripe_webhook, name='stripe_webhook'),
]