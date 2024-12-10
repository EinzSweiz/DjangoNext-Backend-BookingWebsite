from celery import shared_task
from helpers.messaging import send_message
from .models import User
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

@shared_task
def send_confirmation_message(user_id):
    try:
        user = User.objects.get(pk=user_id)
        token = default_token_generator.make_token(user)
        confirmation_url = f"{settings.FRONTEND_URL}/email-confirmation?uid={user.id}&token={token}"
        
        subject = 'Please confirm your email address'
        message = (
            f"Hi {user.name},\n\n"
            f"Please confirm your email address by clicking the link below:\n"
            f"{confirmation_url}\n\n"
            f"Thank you!"
        )
        
        send_message(subject, message, 'riad.sultanov.1999@gmail.com', user.email)
    except Exception as e:
        print(f"Error sending confirmation email: {e}")

@shared_task
def send_reset_email(email, reset_url):
    subject = "Reset Your Password - www.diplomaroad.pro"
    message = (
        f"Hello,\n\n"
        f"We received a request to reset your password for your account associated with this email address.\n\n"
        f"You can reset your password by clicking the link below:\n\n"
        f"{reset_url}\n\n"
        f"If you did not request this, no further action is required. However, we recommend that you secure your account if you suspect any unauthorized access.\n\n"
        f"This link will expire in a set time (usually 24 hours).\n\n"
        f"Thank you for using our service.\n\n"
        f"Best regards,\n"
        f"The Your App Name Team\n"
        f"support@diplomaroad.com"
    )
    from_email = "riad.sultanov.1999@gmail.com"  # Replace with your official email address
    
    send_message(subject, message, from_email, email)
