from rest_framework import serializers
from .models import Property, Reservation, PropertyImage
from useraccounts.serializers import UserModelDynamicSerializer

class PropertyImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['image', 'alt_text', 'image_url']

class PropertyModelDynamicSerializer(serializers.ModelSerializer):
    extra_images = PropertyImagesSerializer(many=True, read_only=True)
    landlord = UserModelDynamicSerializer(fields=['id', 'name', 'avatar_url'], many=False, read_only=True)
    image_url = serializers.SerializerMethodField()
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def get_image_url(self, obj):
        return obj.image_url()

    class Meta:
        model = Property
        fields = '__all__'
    
class ReservationListSerializer(serializers.ModelSerializer):
    property = PropertyModelDynamicSerializer(read_only=True, fields=[
            'id',
            'title',
            'description',
            'price_per_night',
            'image_url',
            'bedrooms',
            'bathrooms',
            'guests',
            'landlord',
            'extra_images',], many=False)
    class Meta:
        model = Reservation
        fields = (
            'id', 'start_date', 'end_date', 'number_of_nights', 'total_price', 'property'
        )