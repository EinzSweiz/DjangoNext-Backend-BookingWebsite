from django.urls import path
from . import api


urlpatterns = [
    path('', api.ConversationListAPIView.as_view(), name='api_conversations_list'),
    path('start/<uuid:user_id>/', api.ConversationStartAPIView.as_view(), name='api_conversation_start'),
    path('<uuid:pk>/', api.ConversationDetailAPIView.as_view(), name='api_conversations_detail')
]