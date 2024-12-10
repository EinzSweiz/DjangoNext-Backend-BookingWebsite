from django.core.mail import EmailMessage

def send_message(subject, message, from_email, to_email, attachment_name=None, attachment_content=None, attachment_mime_type=None, html_message=None):
    # Create the email message
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=from_email,
        to=[to_email]
    )
    if html_message:
        email.content_subtype = 'html'  # Set content type to HTML
        email.body = html_message  # Use the HTML content
    # Attach the file if provided
    if attachment_name and attachment_content:
        email.attach(attachment_name, attachment_content, attachment_mime_type)

    # Send the email
    email.send(fail_silently=False)
