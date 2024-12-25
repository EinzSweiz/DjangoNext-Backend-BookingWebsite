from django import forms
from .models import Property, PropertyImage

class PropertyForm(forms.ModelForm):
    extra_images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = Property
        fields = (
            'title',
            'description',
            'price_per_night',
            'bedrooms',
            'bathrooms',
            'guests',
            'country',
            'country_code',
            'category',
            'image',
        )
