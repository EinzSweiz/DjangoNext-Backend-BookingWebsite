from rest_framework import serializers
from .models import Review, ReviewReport
from useraccounts.serializers import UserDetailSerializer
from property.serializers import PropertyDetailSerializer


class ReviewViewSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model=Review
        fields = ['id', 'user', 'text', 'created_at']
class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields = ['id', 'text', 'created_at']

class ReviewCreateSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    property = PropertyDetailSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'property', 'text', 'user']  # Include 'user' explicitly


class ReviewReportCreateSerializer(serializers.ModelSerializer):
    review = ReviewDetailSerializer(read_only=True)
    reported_by = UserDetailSerializer(read_only=True)

    class Meta:
        model = ReviewReport
        fields = ['review', 'reported_by', 'reason']

    def validate(self, data):
        if not data.get('reason', '').strip():
            raise serializers.ValidationError({"reason": "A reason is required for reporting a review."})
        return data
