from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
import logging

logger = logging.getLogger(__name__)

predefined_responses = {
    "What is this website about?": {
        "response": "DiplomaRoad is a platform for managing and booking accommodations.",
        "redirect": None,
    },
    "How do I contact support?": {
        "response": "You can contact us at support@diplomaroad.pro.",
        "redirect": None,
    },
    "Show me available properties": {
        "response": "Redirecting you to the properties page...",
        "redirect": "/properties",
    },
}

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def chatbot_response(request):
    # Log raw body before accessing request.data
    try:
        raw_body = request.body.decode('utf-8')
        logger.info("Raw body: %s", raw_body)
    except Exception as e:
        logger.error("Failed to decode raw body: %s", e)

    # Access and log parsed data
    logger.info("Parsed data: %s", request.data)

    # Get the question from the request
    question = request.data.get("question")
    if not question:
        return JsonResponse({"error": "Missing 'question' field"}, status=400)

    # Fetch the predefined response
    response = predefined_responses.get(
        question,
        {"response": "I'm sorry, I don't understand that question.", "redirect": None},
    )
    return JsonResponse(response)
