from rest_framework import serializers
from .models import User
from dj_rest_auth.registration.serializers import RegisterSerializer
from .tasks import send_confirmation_message


class UserModelDynamicSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)  # Include avatar handling
    avatar_url = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def get_avatar_url(self, obj):
        return obj.avatar_url()

    class Meta:
        model = User
        fields = '__all__'


class SetPasswordSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)
    uid = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    def validate(self, attrs):
        password1 = attrs.get("new_password1")  # Correct field name
        password2 = attrs.get("new_password2")  # Correct field name

        if password1 != password2:
            raise serializers.ValidationError("Passwords do not match.")

        # Optionally, validate the token and uid if needed
        uid = attrs.get("uid")
        token = attrs.get("token")

        # You can add custom validation for the uid and token if necessary
        # For example, check if they are valid or match a user in your database

        return attrs
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(max_length=255)
    avatar = serializers.ImageField(required=False)

    def get_avatar_url(self, obj):
        return obj.avatar_url() if hasattr(obj, 'avatar_url') and obj.avatar_url() else ''
    def save(self, request):
        if not User.objects.filter(email=self.data.get('email')).exists():
            # Call the parent save method to create the user
            user = super().save(request)
            
            # Update the user instance with additional fields
            user.name = self.data.get('name')
            
            # If an avatar is provided, save it
            if 'avatar' in self.data:
                user.avatar = self.data['avatar']
                
            user.is_active = False  # Deactivate the user until confirmation

            # Save the user with the updated fields
            user.save()

            # Trigger the task to send confirmation email
            send_confirmation_message.delay(user.id)

            return user
        else:
            raise serializers.ValidationError("A user with this email already exists.")