from unittest.mock import patch, Mock
from rest_framework import status
from useraccounts.conftest import create_reservation, create_landlord
import pytest

@pytest.mark.django_db
@patch("stripe.checkout.Session.retrieve")
@patch("stripe.Customer.retrieve")
@patch("my_stripe.api.send_invoice_creation_message.delay")
def test_payment_success_view(
    mock_send_invoice_creation_message, 
    mock_stripe_customer_retrieve, 
    mock_stripe_session_retrieve, 
    api_client, 
    create_reservation
):
    # Mock the Celery task
    mock_send_invoice_creation_message.return_value = None

    # Mock Stripe Session and Customer objects
    mock_session = Mock()
    mock_session.customer = "mock_customer_id"
    mock_session.metadata = {
        "property_id": str(create_reservation.property.id),
        "start_date": "2025-01-01",
        "end_date": "2025-01-05",
        "total_price": "400.0",
        "number_of_nights": "4",
        "guests": "2",
        "has_paid": True,
    }
    mock_stripe_session_retrieve.return_value = mock_session

    mock_customer = Mock()
    mock_customer.id = "mock_customer_id"
    mock_customer.email = "testcustomer@example.com"
    mock_customer.name = "Test Customer"
    mock_stripe_customer_retrieve.return_value = mock_customer

    # Test URL with mock session ID
    url = f"/api/stripe/payment/success/?session_id=mock_session_id"

    # Authenticate the user associated with the reservation
    api_client.force_authenticate(user=create_reservation.created_by)

    # Send GET request to the API
    response = api_client.get(url)

    # Assertions for the response
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert response_data["success"] is True

    # Verify the Reservation object in the database
    reservation = create_reservation.property.reservations.last()
    assert reservation is not None
    print(f"Reservation Stripe Checkout ID: {reservation.stripe_checkout_id}")  # Debugging
    assert reservation.stripe_checkout_id == "mock_session_id"
    assert reservation.has_paid is True


@pytest.mark.django_db
def test_payment_cancel_view(api_client, create_reservation):
    """
    Тест для PaymentCancelAPIView.
    """
    reservation = create_reservation
    # Аутентификация
    api_client.force_authenticate(user=reservation.created_by)

    # URL с UUID
    url = f"/api/stripe/payment/cancel/{reservation.id}/"

    # Отправляем GET-запрос
    response = api_client.get(url)

    # Проверяем статус-код
    assert response.status_code == status.HTTP_200_OK

    # Проверяем содержание ответа
    response_data = response.json()
    assert response_data == {
        "success": False,
        "message": f"Payment for reservation {reservation.id} was canceled."
    }
