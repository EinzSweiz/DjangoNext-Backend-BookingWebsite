from django.http import JsonResponse
from .models import Conversation, ConversationMessage
from .serizalizers import ConversationListSerializer, ConversationDetailSerializer, ConversationMessageSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from useraccounts.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .swagger_usecases import conversation_list_response_schema, conversation_start_request_schema, conversation_start_response_schema, conversation_detail_response_schema

@swagger_auto_schema(
    method="get",
    operation_summary="Retrieve Conversations",
    operation_description="Retrieve a list of all conversations for the authenticated user.",
    responses={200: conversation_list_response_schema, 401: "Unauthorized"}
)
@api_view(['GET'])
def conversation_list(request):
    conversations = request.user.conversations.all().order_by('-modified_at')
    serializer = ConversationListSerializer(
        conversations, 
        many=True, 
        context={'request': request}
    )
    return JsonResponse(serializer.data, safe=False)


@swagger_auto_schema(
    method="get",
    operation_summary="Retrieve Conversation Details",
    operation_description="Retrieve details of a specific conversation, including all messages.",
    responses={200: conversation_detail_response_schema, 404: "Conversation Not Found"}
)
@api_view(['GET'])
def conversations_detail(request, pk): 
    conversation = request.user.conversations.get(pk=pk)
    user = request.user
    conversation.messages.exclude(read_by=user).update()  
    for msg in conversation.messages.exclude(read_by=user):
        msg.read_by.add(user)

    conversation_serializer = ConversationDetailSerializer(conversation, many=False)
    messages_serializer = ConversationMessageSerializer(conversation.messages.all(), many=True)
    return JsonResponse({
        'conversation': conversation_serializer.data,
        'messages': messages_serializer.data
    }, safe=False)



@swagger_auto_schema(
    method="get",
    operation_summary="Start or Retrieve a Conversation",
    operation_description="Start a new conversation with a specific user, or retrieve the existing conversation if one exists.",
    manual_parameters=[
        openapi.Parameter(
            "user_id", openapi.IN_QUERY, 
            description="ID of the user to start a conversation with.", 
            type=openapi.TYPE_INTEGER
        )
    ],
    responses={200: conversation_start_response_schema, 404: "User Not Found"}
)
@api_view(['GET'])
def conversation_start(request, user_id):
    conversation = Conversation.objects.filter(users__in=[user_id]).filter(users__in=[request.user.id])
    if conversation.count() > 0:
        conversation = conversation.first()
        return JsonResponse({'success': True, 'conversation_id': conversation.id})
    else:
        user = User.objects.get(pk=user_id)
        conversation = Conversation.objects.create()
        conversation.users.add(request.user)
        conversation.users.add(user)
        return JsonResponse({'success': 200, 'conversation_id': conversation.id})