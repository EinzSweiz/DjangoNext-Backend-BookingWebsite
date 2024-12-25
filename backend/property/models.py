import uuid
from django.db import models
from django.conf import settings

from useraccounts.models import User


class Property(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price_per_night = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    guests = models.IntegerField()
    country = models.CharField(max_length=255)
    country_code = models.CharField(max_length=10)
    favorited = models.ManyToManyField(User, related_name='favorites', blank=True)
    category = models.CharField(max_length=255)
    image = models.ImageField(upload_to='uploads/properties')
    landlord = models.ForeignKey(User, related_name='properties', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def image_url(self):
        return f'{settings.WEBSITE_URL}{self.image.url}'

class PropertyImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey('Property', related_name='extra_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/properties/extra_images/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    def image_url(self):
        return f"{settings.WEBSITE_URL}{self.image.url}"

    def __str__(self):
        return f"Extra image for {self.property.title}"
    
    
class Reservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, related_name='reservations', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date  = models.DateField()
    number_of_nights = models.IntegerField()
    guests = models.IntegerField(default=1)
    total_price = models.FloatField()
    stripe_checkout_id = models.CharField(max_length=255, null=True, blank=True)  # New field
    has_paid = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='reservations', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
