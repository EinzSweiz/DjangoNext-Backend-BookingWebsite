import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_landlord_detail_success(api_client, create_landlord):
    landlord_id = create_landlord.id
    url = f'/api/auth/{landlord_id}/'
    response = api_client.get(url)
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(landlord_id)
    assert data["name"] == "Test Landlord"
    assert "avatar_url" in data

@pytest.mark.django_db
def test_reservations_list(api_client: APIClient, create_landlord, create_reservation):
    api_client.force_authenticate(user=create_landlord)
    # Define the endpoint URL
    url = '/api/auth/myreservations/'
    response = api_client.get(url)

    # Assert the response
    assert response.status_code == 200
    data = response.json()

    # Validate the data
    assert len(data) == 1
    reservation_data = data[0]
    assert reservation_data["id"] == str(create_reservation.id)
    assert reservation_data["start_date"] == "2025-01-01"
    assert reservation_data["end_date"] == "2025-01-05"
    assert reservation_data["number_of_nights"] == 4
    assert reservation_data["total_price"] == 400.0

    # Validate nested property data
    property_data = reservation_data["property"]
    assert property_data["id"] == str(create_reservation.property.id)
    assert property_data["title"] == "Test Property"
    assert property_data["description"] == "A beautiful test property."
    assert property_data["price_per_night"] == 100
    assert property_data["bedrooms"] == 2
    assert property_data["bathrooms"] == 1


@pytest.mark.django_db
def test_profile_detail(api_client:APIClient, create_landlord):
    user = create_landlord
    api_client.force_authenticate(user=user)
    url = f'/api/auth/profile/{user.id}/'
    repsonse = api_client.get(url)
    assert repsonse.status_code == 200
    data = repsonse.json()

    assert data['id'] == str(user.id)
    assert data['email'] == 'testemail@test.com'
    assert data['name'] == 'Test Landlord'
    assert 'avatar_url' in data


@pytest.mark.django_db
def test_update_profile(api_client:APIClient, create_landlord):
    user = create_landlord
    api_client.force_authenticate(user=user)
    url = f'/api/auth/profile/update/{user.id}'
    data = {
        'name': 'Updated Name',  # Update the name
        # Optionally add an avatar file here if you want to test image uploading
        # 'avatar': <image_file>,
    }
    response = api_client.put(url, data=data)

    assert response.status_code == 200

    updated_data = response.json()

    assert updated_data['name'] == 'Updated Name'
    assert 'avatar' in updated_data or 'avatar_url' in updated_data



