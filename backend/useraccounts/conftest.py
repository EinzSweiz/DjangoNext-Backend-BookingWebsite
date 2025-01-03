import os
import django
from django.core.management import call_command
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile

# Set the default settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.django_backend.settings")

django.setup()

import pytest
from rest_framework.test import APIClient
from useraccounts.models import User
from property.models import Reservation, Property
from uuid import uuid4

@pytest.fixture(scope="session", autouse=True)
def apply_migrations(django_db_setup, django_db_blocker):
    """Apply migrations at the beginning of the test session."""
    with django_db_blocker.unblock():
        call_command("migrate", verbosity=0, interactive=False)

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture(scope="function")
def create_landlord(db):
    """Fixture to create a landlord."""
    return User.objects.create(
        id=uuid4(),
        email="testemail@test.com",
        name="Test Landlord",
        is_verified=True,
        role=User.RoleChoises.ADMIN.value,
    )

@pytest.fixture(scope="function")
@pytest.fixture(scope="function")
def create_reservation(db, create_landlord):
    """Fixture to create a reservation."""
    with tempfile.NamedTemporaryFile(suffix='jpg') as temp_image:
        temp_image.write(b"mock image content")
        temp_image.seek(0)
        mock_image = SimpleUploadedFile(name='test_image.jpg', content=temp_image.read(), content_type='image/jpeg')

        # Create the property
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

        # Create the reservation
        reservation_instance = Reservation.objects.create(
            id=uuid4(),
            property=property_instance,
            start_date="2025-01-01",
            end_date="2025-01-05",
            number_of_nights=4,
            guests=2,
            total_price=400.0,
            stripe_checkout_id=None,
            has_paid=False,
            created_by=create_landlord,
        )

        yield reservation_instance

        # Cleanup logic
        # Delete the reservation
        reservation_instance.delete()

        # Delete the property and its associated image
        if property_instance.image:
            image_path = property_instance.image.path
            if os.path.exists(image_path):
                os.remove(image_path)
        property_instance.delete()
