from rest_framework import serializers
from .models import Inquiry, Message
from useraccounts.models import User

class CreateInquirySerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)  # Email is only for creating the user relation

    class Meta:
        model = Inquiry
        fields = ('subject', 'message', 'email') 

    def create(self, validated_data):
        email = validated_data.pop('email')
        user = User.objects.filter(email=email).first()

        if user:
            validated_data['user'] = user  # Associate the user
        else:
            raise serializers.ValidationError("User with this email does not exist in our system.")

        # Create and return the inquiry
        inquiry = Inquiry.objects.create(**validated_data)
        return inquiry

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField()
    message = serializers.CharField()
    timestamp = serializers.DateTimeField(required=False)

    class Meta:
        model = Message
        fields = ['sender', 'message', 'timestamp']

class CustomerServiceAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']
        
class GetInquirySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name')  # If you want to include the user's name
    user_email = serializers.EmailField(source='user.email')
    messages = MessageSerializer(many=True)

    class Meta:
        model = Inquiry
        fields = ('id', 'subject', 'message', 'response', 'status', 'created_at', 'updated_at', 'user_name', 'messages', 'user_email')


class UpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = ('id', 'status')

    def validate_status(self, value):
        valid_statuses = ['open', 'in_progress', 'closed']  # Add valid statuses for your business logic
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Invalid status: {value}. Valid statuses are {valid_statuses}.")
        return value


class AssignInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = ['customer_service']
