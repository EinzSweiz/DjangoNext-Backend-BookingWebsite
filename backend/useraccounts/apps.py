from django.apps import AppConfig


class UseraccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'useraccounts'

    def ready(self):
        import useraccounts.signals