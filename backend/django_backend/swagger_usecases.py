from drf_yasg import openapi

# Reusable schema for chatbot POST requests
chatbot_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "question": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="The user's question to the chatbot."
        )
    },
    required=["question"]
)

# Reusable schema for chatbot POST responses
chatbot_response_schema = openapi.Response(
    description="Chatbot's response to the user's question.",
    examples={
        "application/json": {
            "response": "DiplomaRoad is a platform for managing and booking accommodations.",
            "redirect": "/aboutus",
            "action": None,
        }
    },
)

# Reusable schema for chatbot GET responses
chatbot_questions_schema = openapi.Response(
    description="A list of all available chatbot questions.",
    examples={
        "application/json": {
            "questions": [
                "What is this website about?",
                "How do I contact support?",
                "How can I check my reservations?",
            ]
        }
    },
)
