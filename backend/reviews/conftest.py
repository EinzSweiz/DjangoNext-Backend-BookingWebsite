import os
import django
import tempfile
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from .models import Review


# Set the default settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.django_backend.settings")

django.setup()

import pytest
from rest_framework.test import APIClient
from useraccounts.models import User
from property.models import Property
from uuid import uuid4

@pytest.fixture(scope='function')
def create_user(db):
    return User.objects.create(
        id=uuid4(),
        email="testemail@test.com",
        name="Test Landlord",
        is_verified=True,
        role=User.RoleChoises.ADMIN.value,
    )

@pytest.fixture(scope='function')
def create_customer_service(db):
    return User.objects.create(
        id=uuid4(),
        email="testcsemail@test.com",
        name="Test CS",
        is_verified=True,
        role=User.RoleChoises.CUSTOMER_SERVICE.value,
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
    

@pytest.fixture
def create_review(api_client, create_user, create_property):
    """
    Helper fixture to create a review and return the review data.
    """
    user = create_user
    property_instance = create_property

    # Test URL
    url = f'/api/reviews/create/{str(property_instance.id)}'

    # Authenticate the user
    api_client.force_authenticate(user=user)

    # Request payload
    review_data = {
        "text": "This is a test review.",
    }

    # Send POST request
    response = api_client.post(url, data=review_data)

    # Debugging
    print(f"Request Data: {review_data}")
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.content.decode()}")

    # Assertions
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get('success') == 'Review was created successfully'

    # Retrieve the created review from the database
    return Review.objects.get(user=user, property=property_instance)

@pytest.fixture
def create_report_review(db, create_user, create_review, api_client: APIClient):
    """
    Fixture to create a report for a review.
    """
    user = create_user
    review = create_review
    
    api_client.force_authenticate(user=user)
    
    url = f'/api/reviews/report/create/{review.id}/'
    
    report_data = {
        "reason": "Inappropriate content",
    }
    
    response = api_client.post(url, data=report_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    
    return response.json()
