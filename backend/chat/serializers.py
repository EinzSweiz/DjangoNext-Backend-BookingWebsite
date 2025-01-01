from rest_framework import serializers
from .models import Conversation, ConversationMessage
from useraccounts.serializers import UserModelDynamicSerializer

class ConversationDynamicSerializer(serializers.ModelSerializer):
    has_unread_messages = serializers.SerializerMethodField()
    users = UserModelDynamicSerializer(fields=['id', 'name', 'avatar_url'], many=True, read_only=True)

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def get_has_unread_messages(self, obj):
        """
        Only include the `has_unread_messages` field when it's needed.
        """
        if 'request' in self.context:
            user = self.context['request'].user
            return obj.messages.exclude(read_by=user).exists()
        return False

    class Meta:
        model = Conversation
        fields = '__all__'

class ConversationMessageSerializer(serializers.ModelSerializer):
    sent_to = UserModelDynamicSerializer(fields=['id', 'name', 'avatar_url'], many=False, read_only=True)
    created_by = UserModelDynamicSerializer(fields=['id', 'name', 'avatar_url'], many=False, read_only=True)
    class Meta:
        model = ConversationMessage
        fields = ('id', 'body', 'sent_to', 'created_by')