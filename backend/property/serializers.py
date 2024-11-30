from rest_framework import serializers
from .models import Property, Reservation
from useraccounts.serializers import UserDetailSerializer

class PropertyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = (
            'id',
            'title',
            'price_per_night',
            'image_url'
        )

class PropertyDetailSerializer(serializers.ModelSerializer):
    landlord = UserDetailSerializer(read_only=True, many=False)
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
        )

class ResirvationListSerializer(serializers.ModelSerializer):
    property = PropertyListSerializer(read_only=True, many=False)
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