from django.contrib import admin
from .models import Review, ReviewReport


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['property', 'text', 'created_at']