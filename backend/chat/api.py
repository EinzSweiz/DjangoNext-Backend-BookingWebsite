from rest_framework.views import APIView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Conversation
from .serializers import ConversationMessageSerializer, ConversationDynamicSerializer
from useraccounts.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .swagger_usecases import (
    conversation_list_response_schema,
    conversation_start_response_schema,
    conversation_detail_response_schema,
)

class ConversationListAPIView(APIView):
    """
    Retrieve a list of all conversations for the authenticated user.
    """
    @swagger_auto_schema(
        operation_summary="Retrieve Conversations",
        operation_description="Retrieve a list of all conversations for the authenticated user.",
        responses={200: conversation_list_response_schema, 401: "Unauthorized"},
    )
    def get(self, request):
        conversations = request.user.conversations.all().order_by('-modified_at')
        serializer = ConversationDynamicSerializer(
            conversations,
            fields=['id', 'users', 'modified_at', 'has_unread_messages'],
            many=True,
            context={'request': request},
        )
        return JsonResponse(serializer.data, safe=False)


class ConversationDetailAPIView(APIView):
    """
    Retrieve details of a specific conversation, including all messages.
    """
    @swagger_auto_schema(
        operation_summary="Retrieve Conversation Details",
        operation_description="Retrieve details of a specific conversation, including all messages.",
        responses={200: conversation_detail_response_schema, 404: "Conversation Not Found"},
    )
    def get(self, request, pk):
        conversation = get_object_or_404(request.user.conversations, pk=pk)
        user = request.user

        # Mark messages as read by the user
        conversation.messages.exclude(read_by=user).update()
        for msg in conversation.messages.exclude(read_by=user):
            msg.read_by.add(user)

        conversation_serializer = ConversationDynamicSerializer(
            conversation, fields=['id', 'users', 'modified_at'], many=False
        )
        messages_serializer = ConversationMessageSerializer(
            conversation.messages.all(), many=True
        )
        return JsonResponse({
            'conversation': conversation_serializer.data,
            'messages': messages_serializer.data,
        }, safe=False)


class ConversationStartAPIView(APIView):
    """
    Start a new conversation with a specific user, or retrieve the existing conversation if one exists.
    """
    @swagger_auto_schema(
        operation_summary="Start or Retrieve a Conversation",
        operation_description="Start a new conversation with a specific user, or retrieve the existing conversation if one exists.",
        manual_parameters=[
            openapi.Parameter(
                "user_id", openapi.IN_QUERY,
                description="ID of the user to start a conversation with.",
                type=openapi.TYPE_INTEGER,
            )
        ],
        responses={200: conversation_start_response_schema, 404: "User Not Found"},
    )
    def get(self, request, user_id):
        # Check if a conversation already exists
        conversation = Conversation.objects.filter(users__in=[user_id]).filter(users__in=[request.user.id]).first()
        if conversation:
            return JsonResponse({'success': True, 'conversation_id': conversation.id}, safe=False)

        # Create a new conversation
        user = get_object_or_404(User, pk=user_id)
        conversation = Conversation.objects.create()
        conversation.users.add(request.user, user)
        return JsonResponse({'success': True, 'conversation_id': conversation.id}, safe=False)
