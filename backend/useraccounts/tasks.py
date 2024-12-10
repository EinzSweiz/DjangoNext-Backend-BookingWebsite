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
    
    # HTML version of the email message
    message = f"""
    <html>
    <body>
        <h2>Password Reset Request</h2>
        <p>Hello,</p>
        <p>We received a request to reset your password for your account associated with this email address.</p>
        <p>You can reset your password by clicking the link below:</p>
        <a href="{reset_url}" style="padding: 10px 20px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px;">Reset Password</a>
        <p>If you did not request this, no further action is required. However, we recommend that you secure your account if you suspect any unauthorized access.</p>
        <p>This link will expire in 24 hours.</p>
        <p>Thank you for using our service.</p>
        <p>Best regards,</p>
        <p>The Your App Name Team</p>
        <p><a href="mailto:support@diplomaroad.com">support@diplomaroad.com</a></p>
    </body>
    </html>
    """
    
    from_email = "riad.sultanov.1999@gmail.com"
    
    # Send the email with HTML content
    send_message(
        subject,          # Subject of the email
        '',               # Plain text message (leave empty since we are sending HTML)
        from_email,       # Sender email address
        email,          # Recipient email address
        html_message=message  # HTML version of the message
    )