from django.http import JsonResponse
from .models import Conversation, ConversationMessage
from .serizalizers import ConversationListSerializer, ConversationDetailSerializer, ConversationMessageSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from useraccounts.models import User
from rest_framework.pagination import PageNumberPagination


@api_view(['GET'])
def conversation_list(request):
    serializer = ConversationListSerializer(request.user.conversations.all(), many=True)
    return JsonResponse(serializer.data, safe=False)

class StandardPagination(PageNumberPagination):
    page_size = 10

@api_view(['GET'])
def conversations_detail(request, pk):
    try:
        conversation = request.user.conversations.get(pk=pk)
    except Conversation.DoesNotExist:
        return JsonResponse({'error': 'Conversation not found'}, status=404)

    conversation_serializer = ConversationDetailSerializer(conversation, many=False)
    paginator = StandardPagination()
    paginated_messages = paginator.paginate_queryset(conversation.messages.all(), request)
    messages_serializer = ConversationMessageSerializer(paginated_messages, many=True)

    return paginator.get_paginated_response({
        'conversation': conversation_serializer.data,
        'messages': messages_serializer.data
    })


@api_view(['GET'])
def conversation_start(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    conversation = Conversation.objects.filter(users=request.user).filter(users=user).first()

    if conversation:
        return JsonResponse({'success': True, 'conversation_id': conversation.id})
    else:
        conversation = Conversation.objects.create()
        conversation.users.add(request.user, user)
        return JsonResponse({'success': True, 'conversation_id': conversation.id})
