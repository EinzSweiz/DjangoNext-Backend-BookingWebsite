from rest_framework import serializers
from .models import Property, Reservation, PropertyImage
from useraccounts.serializers import UserModelDynamicSerializer

class PropertyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = (
            'id',
            'title',
            'price_per_night',
            'image_url',
            'country',
        )

class PropertyImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['image', 'alt_text', 'image_url']

class PropertyDetailSerializer(serializers.ModelSerializer):
    extra_images = PropertyImagesSerializer(many=True, read_only=True)
    landlord = UserModelDynamicSerializer(fields=['id', 'name', 'avatar_url'], many=False, read_only=True)
    class Meta:
        model = Property
        fields = (
            'id',
            'title',
            'description',
            'price_per_night',
            'image_url',
            'bedrooms',
            'bathrooms',
            'guests',
            'landlord',
            'extra_images',
        )

class ResirvationListSerializer(serializers.ModelSerializer):
    property = PropertyDetailSerializer(read_only=True, many=False)
    class Meta:
        model = Reservation
        fields = (
            'id', 'start_date', 'end_date', 'number_of_nights', 'total_price', 'property'
        )

class BookingSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    number_of_nights = serializers.IntegerField()
    guests = serializers.IntegerField()
    has_paid = serializers.BooleanField(required=False, default=False)  # Add this field