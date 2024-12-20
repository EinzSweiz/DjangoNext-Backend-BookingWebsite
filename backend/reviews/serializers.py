from rest_framework import serializers
from .models import Review, ReviewReport


class ReviewViewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model=Review
        fields = ['id', 'user', 'text', 'created_at']

class ReviewCreateSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Review
        fields = ['id', 'property', 'text', 'user']
    

class ReviewReportCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ReviewReport
        fields = ['review', 'reported_by', 'reason']

    def validate(self, data):
        if not data['reason']:
            raise serializers.ValidationError("A reason is required for reporting a review.")
        return data