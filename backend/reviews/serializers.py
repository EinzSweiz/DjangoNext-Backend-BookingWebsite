from rest_framework import serializers
from .models import Review, ReviewReport
from useraccounts.serializers import UserModelDynamicSerializer
from property.serializers import PropertyModelDynamicSerializer

class ReviewModelDynamicSerializer(serializers.ModelSerializer):
    user = UserModelDynamicSerializer(fields=['id', 'name', 'avatar_url'], read_only=True)
    property = PropertyModelDynamicSerializer(fields=[
            'id',
            'title',
            'description',
            'price_per_night',
            'image_url',
            'bedrooms',
            'bathrooms',
            'guests',
            'landlord',
            'extra_images',], read_only=True)

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
    
    class Meta:
        model = Review
        fields = '__all__'

class ReviewReportCreateSerializer(serializers.ModelSerializer):
    review = ReviewModelDynamicSerializer(fields=['id', 'text', 'created_at'], read_only=True)
    reported_by = UserModelDynamicSerializer(fields=['id', 'name', 'avatar_url'], read_only=True)

    class Meta:
        model = ReviewReport
        fields = ['review', 'reported_by', 'reason']

    def validate(self, data):
        if not data.get('reason', '').strip():
            raise serializers.ValidationError({"reason": "A reason is required for reporting a review."})
        return data