import pytest
from .models import Inquiry
from rest_framework import status
from rest_framework.test import APIClient
from reviews.conftest import create_user, create_customer_service


@pytest.mark.django_db
def test_create_inquiry(create_inquiry):
    """
    Test creating an inquiry and validating the API response.
    """
    inquiry = create_inquiry

    # Verify the inquiry exists in the database
    assert inquiry is not None
    assert inquiry.subject == "This is a test subject."
    assert inquiry.message == "This is a test message."

@pytest.mark.django_db
def test_inquiries_get(api_client, create_inquiry):
    """
    Test retrieving inquiries for the authenticated user.
    """
    inquiry = create_inquiry

    # Authenticate the user associated with the inquiry
    user = inquiry.user
    api_client.force_authenticate(user=user)

    # API endpoint to retrieve inquiries
    url = '/api/inquiries/get/'

    # Send GET request
    response = api_client.get(url)

    # Assert the response status code
    assert response.status_code == status.HTTP_200_OK

    # Parse the response data
    response_data = response.json()

    # Debugging: Print the response content
    print(f"Response Data: {response_data}")

    # Assertions for the data structure and content
    assert len(response_data) > 0  # Ensure at least one inquiry is returned
    assert response_data[0]["subject"] == inquiry.subject
    assert response_data[0]["message"] == inquiry.message
    assert response_data[0]["user_email"] == inquiry.user.email
    assert response_data[0]["user_name"] == inquiry.user.name


@pytest.mark.django_db
def test_add_message(api_client, create_inquiry):
    inquiry = create_inquiry

    message_data = {
        "sender": "user",
        "message": "This is a test message",
        "timestamp": "2025-01-04T12:00:00Z",
    }

    url = f'/api/inquiries/add-message/{inquiry.id}/'

    response = api_client.post(url, data=message_data, format='json')
    print('Response:', response)
    # Assert response status
    assert response.status_code == 201

    # Verify database state
    inquiry.refresh_from_db()
    assert inquiry.messages.count() == 1

    message = inquiry.messages.first()
    assert message.sender == "user"
    assert message.message == "This is a test message"


@pytest.mark.django_db
def test_get_customer_service_agent(api_client: APIClient, create_customer_service):
    user = create_customer_service
    api_client.force_authenticate(user=user)
    url = '/api/inquiries/customer-service-agents/'
    response = api_client.get(url)

    assert response.status_code == 200

    data = response.json()
    # Ensure the response contains a list
    assert isinstance(data, list)
    assert len(data) > 0  # Ensure at least one agent is returned

    # Validate the first agent in the list
    agent_data = data[0]
    assert agent_data['name'] == 'Test CS'
    assert agent_data['email'] == 'testcsemail@test.com'
    assert agent_data['id'] == str(user.id)  # Match the `id` field


@pytest.mark.django_db
def test_update_inquiry_status(api_client:APIClient, create_inquiry, create_user):
    user = create_user
    inquiry = create_inquiry

    api_client.force_authenticate(user=user)

    review_data = {
        "status": "active",
    }

    url = f'/api/inquiries/update-status/{inquiry.id}/'

    response = api_client.put(url, data=review_data)

    assert response.status_code == 200


import pytest
from .models import Inquiry
from rest_framework import status

@pytest.mark.django_db
def test_get_inquiry(api_client: APIClient, create_inquiry, create_user):
    """
    Test retrieving a specific inquiry and validating the API response structure and values.
    """
    user = create_user
    inquiry = create_inquiry

    # API endpoint to retrieve a specific inquiry
    url = f'/api/inquiries/get/{inquiry.id}/'
    api_client.force_authenticate(user=user)

    # Send GET request
    response = api_client.get(url)

    # Assert the response status code
    assert response.status_code == 200

    # Parse the response data
    response_data = response.json()

    # Debugging: Print the response content
    print(f"Response Data: {response_data}")

    # Assertions for the response structure and values
    assert response_data["id"] == inquiry.id
    assert response_data["subject"] == inquiry.subject
    assert response_data["message"] == inquiry.message
    assert response_data["response"] == inquiry.response  # Assuming this field is nullable/optional
    assert response_data["status"] == inquiry.status

    # Normalize the timestamps to account for format differences
    assert response_data["created_at"] == inquiry.created_at.isoformat().replace('+00:00', 'Z')
    assert response_data["updated_at"] == inquiry.updated_at.isoformat().replace('+00:00', 'Z')

    # Additional assertions as needed
