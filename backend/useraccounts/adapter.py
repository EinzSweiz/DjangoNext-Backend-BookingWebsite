from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.models import EmailAddress
from .models import User  # Import your custom User model

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Handle social login logic:
        - Check for existing users.
        - Save the user object explicitly if it doesn't exist.
        - Create or update the EmailAddress model.
        """

        # Step 1: Check if a user with the social email already exists
        existing_user = User.objects.filter(email=sociallogin.user.email).first()
        if existing_user:
            # Use the existing user
            sociallogin.user = existing_user
            print(f"Existing user found: {existing_user.email}")
        else:
            # If no existing user, ensure the email is set properly
            print("No existing user found. Ensuring email is set.")
            if not sociallogin.user.email:
                sociallogin.user.email = sociallogin.account.extra_data.get('email')

            if not sociallogin.user.email:
                raise AssertionError("Email not set properly for the user during social login.")

            # Save the user to ensure it has a valid database ID
            sociallogin.user.save()
            print(f"New user saved with email: {sociallogin.user.email}")

        # Step 2: Handle the EmailAddress model
        email_address = EmailAddress.objects.filter(email=sociallogin.user.email).first()
        if email_address:
            # If the email already exists, mark it as verified
            if not email_address.verified:
                email_address.verified = True
                email_address.save()
                print(f"EmailAddress verified: {email_address.email}")
        else:
            # If the email does not exist, create a new EmailAddress entry
            EmailAddress.objects.create(
                user=sociallogin.user,
                email=sociallogin.user.email,
                verified=True
            )
            print(f"EmailAddress created and verified: {sociallogin.user.email}")

        # Step 3: Call the parent method to continue with the social login flow
        print("Calling parent method to finalize social login.")
        return super().pre_social_login(request, sociallogin)
