from django.contrib import admin
from .models import Inquiry, Message



@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['subject', 'message', 'response', 'status', 'created_at']

@admin.register(Message)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['inquiry', 'sender', 'message', 'timestamp']