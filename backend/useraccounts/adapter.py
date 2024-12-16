from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.models import EmailAddress
from allauth.account.utils import setup_user_email
from .models import User

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Debug: Log when the social login process starts
        print(f"Starting pre_social_login for user: {sociallogin.user}")
        
        # Check if the user already exists with the social email
        existing_user = User.objects.filter(email=sociallogin.user.email).first()
        if existing_user:
            print(f"Existing user found: {existing_user}")
            sociallogin.user = existing_user
            sociallogin.save(request)  # Save the user and avoid the signup flow
            print(f"User saved to sociallogin: {sociallogin.user}")
        else:
            print("No existing user found with the given email.")
        
        # Ensure the email is correctly set
        if not sociallogin.user.email:
            sociallogin.user.email = sociallogin.account.extra_data.get('email')
            print(f"Email set from social account extra data: {sociallogin.user.email}")

        if not sociallogin.user.email:
            print("Email is still not set properly, raising AssertionError.")
            raise AssertionError("Email not set properly for the user during social login.")
        
        # Log email assignment process
        print(f"Final email to be used for the user: {sociallogin.user.email}")
        
        # Handle the email in the EmailAddress model
        email_address = EmailAddress.objects.filter(email=sociallogin.user.email).first()
        if email_address:
            print(f"Email address already exists: {email_address}")
            # Email exists, mark it as verified if needed
            email_address.verified = True
            email_address.save()
            print(f"Email address marked as verified: {email_address}")
        else:
            print(f"No existing email address found for {sociallogin.user.email}, creating new one.")
            # If the email does not exist in the EmailAddress model, create it
            email_address = EmailAddress.objects.create(user=sociallogin.user, email=sociallogin.user.email, verified=True)
            print(f"New email address created: {email_address}")
        
        # Debug: Log the status of the email addresses
        all_email_addresses = EmailAddress.objects.filter(user=sociallogin.user)
        print(f"All email addresses for user {sociallogin.user}: {all_email_addresses}")
        
        # Skip calling setup_user_email to avoid the assertion error
        # setup_user_email(request, sociallogin.user, sociallogin.user.email_addresses)
        
        # Call the parent method to continue with the social login
        print("Calling parent pre_social_login to continue with the login process.")
        return super().pre_social_login(request, sociallogin)
