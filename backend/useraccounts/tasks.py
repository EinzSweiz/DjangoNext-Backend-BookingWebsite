from celery import shared_task
from helpers.messaging import send_message
from .models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

@shared_task
def send_confirmation_message(user_id):
    try:
        user = User.objects.get(pk=user_id)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(str(user.id).encode())
        confirmation_url = f'http://{get_current_site(None).domain}/confirm/{uid}/{token}/'
        subject = 'Please confirm your email address'
        message = render_to_string('email/confirmation_email.html', {
            'user': user,
            'confirmation_url': confirmation_url
        })
        
        send_message(subject, message, 'from@example.com', [user.email])
    except Exception as e:
        print(f"Error sending confirmation email: {e}")