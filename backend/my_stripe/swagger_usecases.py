from drf_yasg import openapi

# Schema for Payment Success Response
payment_success_response = openapi.Response(
    description="Details of a successful payment.",
    examples={
        "application/json": {
            "success": True,
            "reservation": {
                "id": 1,
                "start_date": "2024-01-01",
                "end_date": "2024-01-07",
                "total_price": 1000.00,
                "number_of_nights": 6,
                "guests": 2,
                "has_paid": True,
                "created_by": "John Doe",
                "property": {
                    "id": 1,
                    "name": "Luxury Villa",
                    "address": "Bali, Indonesia",
                    "image_url": "https://example.com/property.jpg"
                }
            },
            "customer": {
                "id": "cus_12345",
                "email": "customer@example.com",
                "name": "Jane Smith"
            }
        }
    }
)

# Schema for Payment Cancel Response
payment_cancel_response = openapi.Response(
    description="Response indicating that the payment was canceled.",
    examples={
        "application/json": {
            "success": False,
            "message": "Payment was canceled"
        }
    }
)

# Schema for Stripe Webhook Response
stripe_webhook_response = openapi.Response(
    description="Response for handling Stripe webhooks.",
    examples={
        "application/json": {
            "status": "success"
        }
    }
)
