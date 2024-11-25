from django.core.mail import send_mail


def send_message(subject, message, from_email, to_email):
    send_mail(subject, message, from_email, [to_email])