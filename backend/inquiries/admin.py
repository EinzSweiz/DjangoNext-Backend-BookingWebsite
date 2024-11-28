from django.contrib import admin
from .models import Inquiry



@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['subject', 'message', 'response', 'status', 'created_at']