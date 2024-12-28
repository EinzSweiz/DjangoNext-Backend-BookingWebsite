import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ConversationMessage
import logging

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        token = self.scope.get('query_string', '').decode()
        if not token:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        event = data.get('event')

        if event == "typing":
            name = data['data'].get('name')
            sent_to_id = data['data'].get('sent_to_id')
            conversation_id = data['data'].get('conversation_id')

            if not sent_to_id or not name:
                return await self.send(text_data=json.dumps({
                    'error': 'sent_to_id and name are required for typing event'
                }))

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_typing',
                    'name': name,
                    'conversation_id': conversation_id,
                }
            )
            return

        if event == "chat_message":
            name = data['data'].get('name')
            body = data['data'].get('body')
            sent_to_id = data['data'].get('sent_to_id')
            conversation_id = data['data'].get('conversation_id')

            if not sent_to_id or not name or not body:
                return await self.send(text_data=json.dumps({
                    'error': 'sent_to_id, name, and body are required for chat_message'
                }))

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'body': body,
                    'name': name,
                }
            )
            await self.save_message(conversation_id, body, sent_to_id)

    async def chat_typing(self, event):
        name = event['name']
        conversation_id = event['conversation_id']

        await self.send(text_data=json.dumps({
            'event': 'typing',
            'data': {
                'name': name,
                'conversation_id': conversation_id,
            }
        }))

    async def chat_message(self, event):
        body = event['body']
        name = event['name']

        await self.send(text_data=json.dumps({
            'body': body,
            'name': name
        }))

    @sync_to_async
    def save_message(self, conversation_id, body, sent_to_id):
        user = self.scope['user']
        ConversationMessage.objects.create(
            conversation_id=conversation_id,
            body=body,
            sent_to_id=sent_to_id,
            created_by=user
        )
