from rest_framework import serializers
from .models import User
from dj_rest_auth.registration.serializers import RegisterSerializer
from .tasks import send_confirmation_message


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'password1', 'password2']

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords must match.")
        return data


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'avatar_url']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)

    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['name', 'avatar', 'avatar_url']

    def get_avatar_url(self, obj):
        return obj.avatar_url() if hasattr(obj, 'avatar_url') and obj.avatar_url() else ''


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

            
