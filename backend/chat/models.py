import uuid
from django.db import models
from useraccounts.models import User

class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    users = models.ManyToManyField(User, related_name='conversations')
    created = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class ConversationMessage(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    body = models.TextField()
    sent_to = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
