from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount, SocialToken
from allauth.account.models import EmailAddress
import uuid
from .models import User  # Import your custom User model
import logging

logger = logging.getLogger(__name__)


def generate_unique_anonymous_name():
    """Generates a unique anonymous name using UUID."""
    return f'Anon-{uuid.uuid4().hex[:8]}'  # e.g., Anon-a1b2c3d4
class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):

    def populate_user(self, request, sociallogin, data):
        """
        Populate the user instance with additional data from the social provider.
        Assign a unique default name and a default avatar if not provided.
        """
        user = super().populate_user(request, sociallogin, data)
        
        # Handle the 'name' field
        if not user.name:
            user.name = generate_unique_anonymous_name()
            logger.debug(f"Assigned default name: {user.name}")
        
        # Handle the 'avatar' field
        if not user.avatar:
            user.avatar = 'uploads/avatars/images.jpeg'  # Ensure this path is correct
            logger.debug(f"Assigned default avatar for user: {user.email}")
        
        return user

    def pre_social_login(self, request, sociallogin):
        """
        Handle social login logic:
        - Check for existing users.
        - Save the user object explicitly if it doesn't exist.
        - Create or update the EmailAddress model.
        - Save the SocialToken explicitly to ensure availability.
        """

        # Step 1: Check if a user with the social email already exists
        existing_user = User.objects.filter(email=sociallogin.user.email).first()
        if existing_user:
            sociallogin.user = existing_user
            logger.debug(f"Existing user found: {existing_user.email}")
        else:
            logger.debug("No existing user found. Ensuring email is set.")
            if not sociallogin.user.email:
                sociallogin.user.email = sociallogin.account.extra_data.get('email')

            if not sociallogin.user.email:
                raise AssertionError("Email not set properly for the user during social login.")

            # Save the user to ensure it has a valid database ID
            sociallogin.user.save()
            logger.debug(f"New user saved with email: {sociallogin.user.email}")

        # Step 2: Save the SocialAccount (if not already saved)
        if not sociallogin.account.pk:
            sociallogin.account.user = sociallogin.user  # Link to the user
            sociallogin.account.save()
            logger.debug(f"SocialAccount saved for user: {sociallogin.user.email}")

        # Step 3: Handle the EmailAddress model
        email_address = EmailAddress.objects.filter(email=sociallogin.user.email).first()
        if email_address:
            if not email_address.verified:
                email_address.verified = True
                email_address.save()
                logger.debug(f"EmailAddress verified: {email_address.email}")
        else:
            EmailAddress.objects.create(
                user=sociallogin.user,
                email=sociallogin.user.email,
                verified=True
            )
            logger.debug(f"EmailAddress created and verified: {sociallogin.user.email}")

        # Step 4: Save the SocialToken explicitly
        if sociallogin.token:
            token = SocialToken.objects.filter(account=sociallogin.account).first()
            if not token:
                SocialToken.objects.create(
                    account=sociallogin.account,
                    token=sociallogin.token.token,
                    token_secret=getattr(sociallogin.token, 'token_secret', None)
                )
                logger.debug(f"SocialToken saved for user: {sociallogin.user.email}")
            else:
                logger.debug("SocialToken already exists.")

        # Step 5: Finalize the social login
        logger.debug("Calling parent method to finalize social login.")
        return super().pre_social_login(request, sociallogin)
