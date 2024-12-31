from drf_yasg import openapi

# Reusable schema for responses and requests
user_id_schema = openapi.Schema(
    type=openapi.TYPE_STRING,
    description="The unique ID of the user."
)

email_schema = openapi.Schema(
    type=openapi.TYPE_STRING,
    description="User's email address."
)

password_reset_response_schema = openapi.Response(
    description="Password reset email sent successfully.",
    examples={
        "application/json": {
            "message": "Password reset email sent successfully."
        }
    },
)

password_reset_error_schema = openapi.Response(
    description="Error response for password reset.",
    examples={
        "application/json": {
            "error": "No user with this email"
        }
    },
)

set_password_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "new_password1": openapi.Schema(type=openapi.TYPE_STRING, description="New password"),
        "new_password2": openapi.Schema(type=openapi.TYPE_STRING, description="Repeat new password"),
    },
    required=["new_password1", "new_password2"],
)

set_password_response_schema = openapi.Response(
    description="Password reset successfully.",
    examples={
        "application/json": {
            "message": "Password has been reset successfully."
        }
    },
)

user_profile_update_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "name": openapi.Schema(type=openapi.TYPE_STRING, description="User's name"),
        "avatar": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_BINARY, description="Profile avatar (image file)"),
    },
    required=["name"],
)