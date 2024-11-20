from django.http import JsonResponse
from .models import Conversation, ConversationMessage
from .serizalizers import ConversationListSerializer, ConversationDetailSerializer, ConversationMessageSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from useraccounts.models import User

@api_view(['GET'])
def conversation_list(request):
    serializer = ConversationListSerializer(request.user.conversations.all(), many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def conversations_detail(request, pk): 
    conversation = request.user.conversations.get(pk=pk)   
    conversation_serializer = ConversationDetailSerializer(conversation, many=False)
    messages_serializer = ConversationMessageSerializer(conversation.messages.all(), many=True)
    return JsonResponse({
        'conversation': conversation_serializer.data,
        'messages': messages_serializer.data
    }, safe=False)


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