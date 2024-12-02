from django.core.mail import send_mail
from django.core.mail import EmailMessage

def send_message(subject, message, from_email, to_email, attachment_name=None, attachment_content=None, attachment_mime_type=None):
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=[to_email],
        fail_silently=False,
        html_message=message
    )
    
    if attachment_name and attachment_content:
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=[to_email]
        )
        email.attach(attachment_name, attachment_content, attachment_mime_type)
        email.send(fail_silently=False)
