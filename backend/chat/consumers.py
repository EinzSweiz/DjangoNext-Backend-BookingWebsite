import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ConversationMessage


class ChatConsumer(AsyncWebsocketConsumer):  # Fixed typo in class name
    async def connect(self):
        # Get the room name from URL
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Token authentication (example)
        token = self.scope.get('query_string', '').decode()  # Get token from query string
        if not token:
            # Reject connection if no token is provided
            await self.close()
            return
        
        print(f"Received token: {token}")
        # Here, add token validation logic (e.g., decode the JWT token and check if it's valid)
        # If token is invalid, you should also reject the connection

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        # Ensure room_group_name is set before attempting to discard from the group
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        # Parse incoming message
        data = json.loads(text_data)

        conversation_id = data['data'].get('conversation_id')  # Use get() to avoid KeyError
        sent_to_id = data['data'].get('sent_to_id')
        name = data['data'].get('name')
        body = data['data'].get('body')

        # Handle missing fields with error responses
        if not sent_to_id:
            return await self.send(text_data=json.dumps({
                'error': 'sent_to_id is missing'
            }))

        if not name or not body:
            return await self.send(text_data=json.dumps({
                'error': 'name and body are required'
            }))

        # Process message (if all necessary fields are present)
        # Save the message to the database (for example)

        # Send message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'body': body,
                'name': name
            }
        )
        await self.save_message(conversation_id, body, sent_to_id)
    async def chat_message(self, event):
        body = event['body']
        name = event['name']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'body': body,
            'name': name
        }))

    @sync_to_async
    def save_message(self, conversation_id, body, sent_to_id):
        user = self.scope['user']

        ConversationMessage.objects.create(conversation_id=conversation_id, body=body, sent_to_id=sent_to_id, created_by=user)