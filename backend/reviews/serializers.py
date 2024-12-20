from rest_framework import serializers
from .models import Review, ReviewReport
from useraccounts.serializers import UserDetailSerializer
from property.serializers import PropertyDetailSerializer


class ReviewViewSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model=Review
        fields = ['id', 'user', 'text', 'created_at']

class ReviewCreateSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    property = PropertyDetailSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'property', 'text', 'user']  # Include 'user' explicitly


class ReviewReportCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ReviewReport
        fields = ['review', 'reported_by', 'reason']

    def validate(self, data):
        if not data['reason']:
            raise serializers.ValidationError("A reason is required for reporting a review.")
        return data