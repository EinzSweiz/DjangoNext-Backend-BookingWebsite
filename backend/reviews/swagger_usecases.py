from drf_yasg import openapi

# Schema for paginated reviews response
paginated_reviews_schema = openapi.Response(
    description="Paginated list of reviews for a property.",
    examples={
        "application/json": {
            "total_pages": 10,
            "current_page": 1,
            "total_reviews": 50,
            "reviews": [
                {
                    "id": 1,
                    "user": "John Doe",
                    "text": "This is a great property!",
                    "created_at": "2024-01-01T12:00:00Z",
                }
            ]
        }
    }
)

# Schema for review creation request
review_create_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "text": openapi.Schema(type=openapi.TYPE_STRING, description="Review text for the property."),
    },
    required=["text"],
)

# Schema for review creation response
review_create_response_schema = openapi.Response(
    description="Response after successfully creating a review.",
    examples={
        "application/json": {
            "success": "Review was created successfully"
        }
    }
)

# Schema for report creation request
report_create_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "reason": openapi.Schema(type=openapi.TYPE_STRING, description="Reason for reporting the review."),
    },
    required=["reason"],
)

# Schema for report creation response
report_create_response_schema = openapi.Response(
    description="Response after successfully creating a report.",
    examples={
        "application/json": {
            "success": "Report was created successfully"
        }
    }
)
