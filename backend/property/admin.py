from django.contrib import admin
from .models import Property, Reservation, PropertyImage

class PropertyImagesInline(admin.TabularInline):
    model = PropertyImage
    extra = 1

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'country']
    inlines = [PropertyImagesInline]

@admin.register(Reservation)
class PropertyAdmin(admin.ModelAdmin):
    readonly_fields = ['number_of_nights']
    list_display = ['created_by', 'start_date', 'end_date', 'number_of_nights', 'created_at', 'total_price']