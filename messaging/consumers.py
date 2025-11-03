#used chatgpt version 5 to generate and modify this code 
#used https://medium.com/@farad.dev/how-to-build-a-real-time-chat-app-using-django-channels-2ba2621ea972

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import Message

#a class that users get an instance of when they connect, disconnect, or recieve a 
#message 
@database_sync_to_async
def create_message(sender_id, receiver_id, content):
    """Sync ORM helper, run in a thread by channels."""
    return Message.objects.create(
        sender_id=sender_id,
        receiver_id=receiver_id,
        content=content,
    )

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_group_name = f"chat_{self.chat_id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data or "{}")
        sender_id = data.get("sender_id")
        receiver_id = data.get("receiver_id")
        content = data.get("content", "")

        # Save the message in the DB
        msg = await create_message(sender_id, receiver_id, content)

        # Broadcast to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "message_id": msg.id,
                "sender_id": sender_id,
                "receiver_id": receiver_id,
                "content": content,
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

# DMConsumer as an alias
DMConsumer = ChatConsumer
