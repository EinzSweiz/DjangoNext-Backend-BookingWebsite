from django.contrib import admin
from .models import Conversation, ConversationMessage


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['created', 'modified_at']



@admin.register(ConversationMessage)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'sent_to', 'created_by', 'created_at']