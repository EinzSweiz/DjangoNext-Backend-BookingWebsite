from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User



def confirm_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(id=uid)

        if default_token_generator.check_token(user, token):
            user.is_active = True  # Mark the user as active
            user.save()
            messages.success(request, 'Your email has been confirmed.')
        else:
            messages.error(request, 'The confirmation link is invalid or expired.')
    except Exception as e:
        messages.error(request, 'An error occurred while confirming your email.')