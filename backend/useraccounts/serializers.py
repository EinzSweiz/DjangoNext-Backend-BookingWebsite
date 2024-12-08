from rest_framework import serializers
from .models import User
from dj_rest_auth.registration.serializers import RegisterSerializer
from .tasks import send_confirmation_message
from dj_rest_auth.serializers import PasswordResetSerializer
from django.contrib.sites.shortcuts import get_current_site

class CustomPasswordResetSerializer(PasswordResetSerializer):
    def save(self, **kwargs):
        request = self.context.get('request')
        domain_override = 'www.diplomaroad.pro'  # Force your frontend domain
        super().save(domain_override=domain_override, request=request, **kwargs)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}



class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'avatar_url']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'avatar_url']


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

            
