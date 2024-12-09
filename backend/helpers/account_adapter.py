from allauth.account.adapter import DefaultAccountAdapter


class MyAccountAdapter(DefaultAccountAdapter):
    def is_email_verified(self, user):
        if user.socialaccount_set.exists():
            return True
        return super().is_email_verified(user)