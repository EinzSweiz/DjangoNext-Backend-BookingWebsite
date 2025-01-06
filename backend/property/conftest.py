import os
import django
from django.core.management import call_command
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
from useraccounts.conftest import create_landlord

# Set the default settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.django_backend.settings")

django.setup()

import pytest
from rest_framework.test import APIClient
from property.models import Reservation, Property
from uuid import uuid4

from unittest.mock import patch



@pytest.fixture(scope='function')
def create_property(db, create_landlord):
    with tempfile.NamedTemporaryFile(suffix='jpg') as temp_image:
        temp_image.write(b'mock test image')
        temp_image.seek(0)
        mock_image = SimpleUploadedFile(name='test image.jpg', content=temp_image.read(), content_type='image/jpeg')


        property_instance = Property.objects.create(
            id=uuid4(),
            title="Test Property",
            description="A beautiful test property.",
            price_per_night=100,
            bedrooms=2,
            bathrooms=1,
            guests=4,
            country="Testland",
            country_code="TL",
            category="Test Category",
            landlord=create_landlord,
            image=mock_image,
        )
        yield property_instance

        if property_instance.image:
            image_path = property_instance.image.path
            if os.path.exists(image_path):
                os.remove(image_path)
        property_instance.delete()