from rest_framework import serializers
from .models import User, Note


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
        fields = ['id', 'name', 'email', 'avatar_url']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)

    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['name', 'avatar', 'avatar_url']

    def get_avatar_url(self, obj):
        return obj.avatar_url() if hasattr(obj, 'avatar_url') and obj.avatar_url() else ''
