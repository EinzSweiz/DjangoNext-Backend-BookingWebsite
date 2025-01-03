import os
import django
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile

# Set the default settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.django_backend.settings")

django.setup()

import pytest
from rest_framework.test import APIClient
from useraccounts.models import User
from property.models import Property
from uuid import uuid4


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture(scope='function')
def create_user(db):
    return User.objects.create(
        id=uuid4(),
        email="testemail@test.com",
        name="Test Landlord",
        is_verified=True,
        role=User.RoleChoises.ADMIN.value,
    )
@pytest.fixture(scope="function")
def create_property(db, create_user):
    """Fixture to create a property."""
    with tempfile.NamedTemporaryFile(suffix="jpg") as temp_image:
        temp_image.write(b"mock image content")
        temp_image.seek(0)
        mock_image = SimpleUploadedFile(name="test_image.jpg", content=temp_image.read(), content_type="image/jpeg")

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
            landlord=create_user,
            image=mock_image,
        )

        yield property_instance

        # Cleanup logic
        if property_instance.image:
            image_path = property_instance.image.path
            if os.path.exists(image_path):
                os.remove(image_path)

        property_instance.delete()