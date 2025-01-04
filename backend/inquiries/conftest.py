import os
import django
from rest_framework.test import APIClient
from rest_framework import status
from reviews.conftest import create_user
from .models import Inquiry


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.django_backend.settings")

django.setup()

import pytest
from uuid import uuid4

@pytest.fixture(scope='function')
def create_inquiry(db, api_client: APIClient, create_user):
    """
    Fixture to create an inquiry and return the Inquiry object.
    """
    user = create_user
    inquiry_data = {
        "subject": "This is a test subject.",
        "message": "This is a test message.",
        "email": user.email,
    }

    api_client.force_authenticate(user=user)

    url = '/api/inquiries/create/'

    response = api_client.post(url, data=inquiry_data)

    # Assert the response status
    assert response.status_code == status.HTTP_201_CREATED

    # Retrieve and return the created inquiry from the database
    return Inquiry.objects.filter(subject=inquiry_data["subject"], message=inquiry_data["message"], user=user).first()

