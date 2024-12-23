from django.contrib import admin
from .models import Review, ReviewReport


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'property', 'text', 'created_at']


@admin.register(ReviewReport)
class ReviewReportAdmin(admin.ModelAdmin):
    list_display = ['review', 'reported_by', 'reason', 'status', 'created_at']