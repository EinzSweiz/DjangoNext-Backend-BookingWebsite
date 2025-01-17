from drf_yasg import openapi

# Create Inquiry Request Schema
create_inquiry_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "subject": openapi.Schema(type=openapi.TYPE_STRING, description="The subject of the inquiry."),
        "message": openapi.Schema(type=openapi.TYPE_STRING, description="The message content of the inquiry."),
        "email": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description="Email of the user submitting the inquiry."),
    },
    required=["subject", "message", "email"],
)

# Create Inquiry Response Schema
create_inquiry_response_schema = openapi.Response(
    description="Response for creating an inquiry.",
    examples={
        "application/json": {
            "id": 1,
            "subject": "Booking issue",
            "message": "I have a problem with my booking.",
            "severity": "urgent",
            "status": "pending",
            "created_at": "2024-01-01T12:00:00Z",
            "updated_at": "2024-01-01T12:00:00Z",
        }
    },
)

# Get Inquiry List Response Schema
get_inquiries_response_schema = openapi.Response(
    description="List of inquiries for the current user.",
    examples={
        "application/json": [
            {
                "id": 1,
                "subject": "Booking issue",
                "status": "pending",
                "severity": "urgent",
                "created_at": "2024-01-01T12:00:00Z",
                "is_resolved": False,
            },
            {
                "id": 2,
                "subject": "Payment problem",
                "status": "active",
                "severity": "normal",
                "created_at": "2024-01-02T12:00:00Z",
                "is_resolved": True,
            },
        ]
    },
)

# Add Message Request Schema
add_message_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "sender": openapi.Schema(type=openapi.TYPE_STRING, enum=["user", "customer_service"], description="The sender of the message."),
        "message": openapi.Schema(type=openapi.TYPE_STRING, description="The content of the message."),
    },
    required=["sender", "message"],
)

# Add Message Response Schema
add_message_response_schema = openapi.Response(
    description="Response for adding a message to an inquiry.",
    examples={
        "application/json": {
            "id": 1,
            "sender": "user",
            "message": "I need help with my booking.",
            "timestamp": "2024-01-01T12:00:00Z",
        }
    },
)

# Update Inquiry Status Request Schema
update_status_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "status": openapi.Schema(
            type=openapi.TYPE_STRING,
            enum=["active", "pending", "resolved"],
            description="The updated status of the inquiry.",
        ),
        "is_resolved": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Whether the inquiry is resolved."),
    },
)

# Update Inquiry Status Response Schema
update_status_response_schema = openapi.Response(
    description="Response for updating the inquiry status.",
    examples={
        "application/json": {
            "id": 1,
            "status": "resolved",
            "is_resolved": True,
        }
    },
)

# Get Inquiry Details Response Schema
get_inquiry_response_schema = openapi.Response(
    description="Retrieve detailed information about a specific inquiry.",
    examples={
        "application/json": {
            "id": 1,
            "subject": "Booking issue",
            "message": "I have a problem with my booking.",
            "response": "Your booking issue has been resolved.",
            "status": "resolved",
            "created_at": "2024-01-01T12:00:00Z",
            "updated_at": "2024-01-02T15:00:00Z",
            "user_name": "John Doe",
            "user_email": "john.doe@example.com",
            "messages": [
                {
                    "sender": "user",
                    "message": "I have a problem with my booking.",
                    "timestamp": "2024-01-01T12:05:00Z",
                },
                {
                    "sender": "customer_service",
                    "message": "We are looking into your issue.",
                    "timestamp": "2024-01-01T12:15:00Z",
                },
            ],
            "severity": "urgent",
            "customer_service": 3,
            "customer_service_name": "Agent Smith",
            "user_role": "user",
        }
    },
)

# Get Customer Service Agents Response Schema
get_customer_service_agents_response_schema = openapi.Response(
    description="Retrieve a list of all customer service agents.",
    examples={
        "application/json": [
            {"id": 1, "name": "Agent Smith", "email": "agent.smith@example.com"},
            {"id": 2, "name": "Agent Johnson", "email": "agent.johnson@example.com"},
        ]
    },
)