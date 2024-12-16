# in your adapters.py or another appropriate file
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.models import EmailAddress
from allauth.account.utils import user_email
from .models import User

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Check if the user already exists with the social email
        existing_user = User.objects.filter(email=sociallogin.user.email).first()
        if existing_user:
            sociallogin.user = existing_user
            sociallogin.save(request)  # Save the user and avoid the signup flow
        else:
            # Handle case where no existing user is found (you can choose to auto-create if needed)
            pass
        
        # Ensure the email is correctly set, debug the email assignment
        if not sociallogin.user.email:
            sociallogin.user.email = sociallogin.account.extra_data.get('email')
            print(f"Assigning email: {sociallogin.user.email}")  # Debug line

        if not sociallogin.user.email:
            raise AssertionError("Email not set properly for the user during social login.")

        # If the email exists but is not verified, mark it as verified automatically
        email_address = EmailAddress.objects.filter(email=sociallogin.user.email).first()
        if email_address:
            email_address.verified = True
            email_address.save()

        # Call the parent method to continue with the social login
        return super().pre_social_login(request, sociallogin)
