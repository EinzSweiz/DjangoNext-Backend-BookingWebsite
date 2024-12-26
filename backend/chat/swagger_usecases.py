from drf_yasg import openapi

# Conversation List Response Schema
conversation_list_response_schema = openapi.Response(
    description="List of conversations for the authenticated user.",
    examples={
        "application/json": [
            {
                "id": "0e9b5c9d-0a15-4f89-b2ee-8e7296f37eb7",
                "users": [
                    {"id": 1, "name": "John Doe", "email": "john@example.com"},
                    {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
                ],
                "modified_at": "2024-01-01T12:00:00Z"
            },
        ]
    }
)

# Conversation Detail Response Schema
conversation_detail_response_schema = openapi.Response(
    description="Details of a specific conversation and its messages.",
    examples={
        "application/json": {
            "conversation": {
                "id": "0e9b5c9d-0a15-4f89-b2ee-8e7296f37eb7",
                "users": [
                    {"id": 1, "name": "John Doe", "email": "john@example.com"},
                    {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
                ],
                "modified_at": "2024-01-01T12:00:00Z"
            },
            "messages": [
                {
                    "id": "1a3e5c1d-2f49-4329-a3ec-4d238bfbeb67",
                    "body": "Hello!",
                    "sent_to": {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
                    "created_by": {"id": 1, "name": "John Doe", "email": "john@example.com"}
                }
            ]
        }
    }
)

# Start Conversation Request Schema
conversation_start_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "user_id": openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description="ID of the user to start a conversation with."
        )
    },
    required=["user_id"]
)

# Start Conversation Response Schema
conversation_start_response_schema = openapi.Response(
    description="Response for starting or retrieving a conversation.",
    examples={
        "application/json": {
            "success": True,
            "conversation_id": "0e9b5c9d-0a15-4f89-b2ee-8e7296f37eb7"
        }
    }
)
