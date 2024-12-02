from django.urls import path
from . import api
urlpatterns = [
    path('payment/success/', api.payment_success, name='api_payment_success')
]