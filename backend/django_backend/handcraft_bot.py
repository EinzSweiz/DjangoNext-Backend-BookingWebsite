from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .swagger_usecases import (
    chatbot_request_schema,
    chatbot_response_schema,
    chatbot_questions_schema,
)
import logging

logger = logging.getLogger(__name__)

# Predefined responses for chatbot queries
PREDEFINED_RESPONSES = {
    "What is this website about?": {
        "response": "DiplomaRoad is a platform for managing and booking accommodations. Redirecting you now...",
        "redirect": '/aboutus',
    },
    "How do I contact support?": {
        "response": "You can contact us at support@diplomaroad.pro. I will open the contact modal for you now.",
        "action": "open_contact_modal",  # Action for opening the Contact Us modal
    },
     "How can I contact the landlord?": {
        "response": "Please click on any property, then click on the host's name or image, and you will see the contact option. Redirecting you to a property page now...",
        "redirect": "/properties/cf1ed08d-dd86-43fa-8c5b-b4e7116b5d3c",
    },
    "How can I check my reservations?": {
        "response": "You can view your reservations in your profile under the Reservations tab. Redirecting you now...",
        "redirect": "/myreservations",
    },
    "How can I check my favorites?": {
        "response": "You can find your favorited properties in the Favorites tab in your profile. Redirecting you now...",
        "redirect": "/myfavorites",
    },
    "How much time does it take to get a response to an inquiry?": {
        "response": "Our support team typically responds to inquiries within 24-48 hours. You can check everything in 'My Inquiries'. Redirecting you now...",
        "redirect": '/myinquiries',
    },
    "Where is your office located?": {
        "response": "Our office is located at 123 Main Street, Cityville. Check 'Contact Us' for directions. I will open the contact modal for you now.",
        "action": "open_contact_modal",
    },
    "How can I meet with you and visit your office?": {
        "response": "You can schedule a meeting through our 'Contact Us' page or email us at meetings@diplomaroad.pro. I will open the contact modal for you now.",
        "action": "open_contact_modal",
    },
    "What payment methods do you accept?": {
        "response": "We accept Visa, Mastercard, PayPal, and Stripe payments. More methods coming soon!",
        "redirect": None,
    },
    "How can I update my profile information?": {
        "response": "You can update your profile information inside the Profile page. I will open the profile modal for you now.",
        "action": "open_profile_modal",
    },
}

@swagger_auto_schema(
    method="post",
    operation_summary="Chatbot query handler",
    operation_description="Processes chatbot queries and provides predefined responses based on the question.",
    request_body=chatbot_request_schema,
    responses={200: chatbot_response_schema, 400: "Invalid request or missing 'question' field."},
)
@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def chatbot_response(request):
    """Handle chatbot queries and provide predefined responses."""
    question = request.data.get("question")
    if not question:
        return JsonResponse({"error": "Missing 'question' field"}, status=400)

    response = PREDEFINED_RESPONSES.get(
        question,
        {"response": "I'm sorry, I don't understand that question.", "redirect": None, "action": None},
    )
    return JsonResponse(response)


@swagger_auto_schema(
    method="get",
    operation_summary="Retrieve all chatbot questions",
    operation_description="Returns a list of all predefined questions that the chatbot can answer.",
    responses={200: chatbot_questions_schema},
)
@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def get_all_questions(request):
    """Return all available chatbot questions."""
    questions = list(PREDEFINED_RESPONSES.keys())
    return JsonResponse({"questions": questions})