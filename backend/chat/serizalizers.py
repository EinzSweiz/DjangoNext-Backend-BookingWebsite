from rest_framework import serializers
from .models import Conversation, ConversationMessage
from useraccounts.serializers import UserModelDynamicSerializer

class ConversationListSerializer(serializers.ModelSerializer):
    has_unread_messages = serializers.SerializerMethodField()
    users = UserModelDynamicSerializer(fields=['id', 'name', 'avatar_url'], many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ('id', 'users', 'modified_at', 'has_unread_messages')

    def get_has_unread_messages(self, obj):
        user = self.context['request'].user
        return obj.messages.exclude(read_by=user).exists()

class ConversationDetailSerializer(serializers.ModelSerializer):
    users = UserModelDynamicSerializer(fields=['id', 'name', 'avatar_url'], many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ('id', 'users', 'modified_at')


class ConversationMessageSerializer(serializers.ModelSerializer):
    sent_to = UserModelDynamicSerializer(fields=['id', 'name', 'avatar_url'], many=False, read_only=True)
    created_by = UserModelDynamicSerializer(fields=['id', 'name', 'avatar_url'], many=False, read_only=True)
    class Meta:
        model = ConversationMessage
        fields = ('id', 'body', 'sent_to', 'created_by')