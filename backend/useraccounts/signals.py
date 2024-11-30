import stripe
from django.conf import settings
from django.db.models.signals import post_save
from useraccounts.models import User
from django.dispatch import receiver

if settings.DEBUG:
    stripe.api_key = settings.STRIPE_PUBLISH_KEY
else:
    stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_customer(user):
    # Check if user already has a customer ID in your database
    if not user.stripe_customer_id:
        customer = stripe.Customer.create(
            email=user.email,
            name=f"{user.name}",
        )
        user.stripe_customer_id = customer.id
        user.save()  # Save customer ID to your database
    return user.stripe_customer_id

@receiver(post_save, sender=User)
def create_customer_signal(sender, instance, created, **kwargs):
    if created:
        create_stripe_customer(instance)