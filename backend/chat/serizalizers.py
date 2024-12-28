from rest_framework import serializers
from .models import Conversation, ConversationMessage
from useraccounts.serializers import UserDetailSerializer

class ConversationListSerializer(serializers.ModelSerializer):
    has_unread_messages = serializers.SerializerMethodField()
    users = UserDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ('id', 'users', 'modified_at', 'has_unread_messages')
    
    def get_has_unread_messages(self, obj):
        request = self.context.get('request')
        if request:
            user = request.user
            return obj.messages.exclude(read_by=user).exists()
        return False


class ConversationDetailSerializer(serializers.ModelSerializer):
    users = UserDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ('id', 'users', 'modified_at')


class ConversationMessageSerializer(serializers.ModelSerializer):
    sent_to = UserDetailSerializer(many=False, read_only=True)
    created_by = UserDetailSerializer(many=False, read_only=True)
    class Meta:
        model = ConversationMessage
        fields = ('id', 'body', 'sent_to', 'created_by')