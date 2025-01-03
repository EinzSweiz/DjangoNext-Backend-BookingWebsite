import pytest
from rest_framework import status
from property.models import Property

@pytest.mark.django_db
def test_create_review(api_client, create_user, create_property):
    user = create_user
    property_instance = create_property

    # Debugging
    print(f"Testing with Property ID: {property_instance.id}")
    print(f"Property exists in DB: {Property.objects.filter(id=property_instance.id).exists()}")

    # Test URL
    url = f'/api/reviews/create/{str(property_instance.id)}'
    print(f"Test URL: {url}")

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
