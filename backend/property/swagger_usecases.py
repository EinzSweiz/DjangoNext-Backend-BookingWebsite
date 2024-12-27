from drf_yasg import openapi

# Schemas for Property APIs
property_list_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_STRING, description="Property ID"),
        "title": openapi.Schema(type=openapi.TYPE_STRING, description="Property title"),
        "price_per_night": openapi.Schema(type=openapi.TYPE_INTEGER, description="Price per night"),
        "image_url": openapi.Schema(type=openapi.TYPE_STRING, description="URL of the property image"),
        "country": openapi.Schema(type=openapi.TYPE_STRING, description="Country"),

    },
)

property_detail_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_STRING, description="Property ID"),
        "title": openapi.Schema(type=openapi.TYPE_STRING, description="Property title"),
        "description": openapi.Schema(type=openapi.TYPE_STRING, description="Property description"),
        "price_per_night": openapi.Schema(type=openapi.TYPE_INTEGER, description="Price per night"),
        "image_url": openapi.Schema(type=openapi.TYPE_STRING, description="Main property image URL"),
        "bedrooms": openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of bedrooms"),
        "bathrooms": openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of bathrooms"),
        "guests": openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of guests allowed"),
        "landlord": openapi.Schema(type=openapi.TYPE_OBJECT, description="Landlord details"),
        "extra_images": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT)),
    },
)

reservation_list_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_STRING, description="Reservation ID"),
        "start_date": openapi.Schema(type=openapi.TYPE_STRING, format="date", description="Start date of the reservation"),
        "end_date": openapi.Schema(type=openapi.TYPE_STRING, format="date", description="End date of the reservation"),
        "number_of_nights": openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of nights"),
        "total_price": openapi.Schema(type=openapi.TYPE_NUMBER, format="float", description="Total price for the reservation"),
        "property": property_detail_schema,
    },
)

booking_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "start_date": openapi.Schema(type=openapi.TYPE_STRING, format="date", description="Start date for the booking"),
        "end_date": openapi.Schema(type=openapi.TYPE_STRING, format="date", description="End date for the booking"),
        "total_price": openapi.Schema(type=openapi.TYPE_NUMBER, format="float", description="Total price"),
        "number_of_nights": openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of nights"),
        "guests": openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of guests"),
        "has_paid": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Payment status", default=False),
    },
)

favorite_toggle_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "is_favorited": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Favorite status of the property"),
    },
)
