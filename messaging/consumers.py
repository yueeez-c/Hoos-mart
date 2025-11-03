#used chatgpt version 5 to generate and modify this code 
#used https://medium.com/@farad.dev/how-to-build-a-real-time-chat-app-using-django-channels-2ba2621ea972

# messaging/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import Message


@database_sync_to_async
def create_message(sender_id, receiver_id, content):
    return Message.objects.create(
        sender_id=sender_id,
        receiver_id=receiver_id,
        content=content,
    )

async def receive(self, text_data=None, bytes_data=None):
    if not text_data:
        return

    try:
        data = json.loads(text_data)
    except json.JSONDecodeError:
        return  # ignore bad payloads

    content = (data.get("content") or data.get("message") or "").strip()
    if not content:
        return

    user = self.scope.get("user")
    if not user or isinstance(user, AnonymousUser):
        await self.close()
        return

    sender_id = user.id
    try:
        receiver_id = int(self.chat_id)
    except (TypeError, ValueError):
        return

    msg = await create_message(sender_id, receiver_id, content)

    await self.channel_layer.group_send(
        self.room_group_name,
        {
            "type": "chat.message",
            "message_id": msg.id,
            "message": content,
            "sender_id": sender_id,
            "receiver_id": receiver_id,
        },
    )


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # chat_id from URL: /ws/dm/<chat_id>/
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_group_name = f"chat_{self.chat_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return

        data = json.loads(text_data)

        # Support both "content" and "message" keys
        content = (data.get("content") or data.get("message") or "").strip()
        if not content:
            # Don't save empty messages
            return

        # Use the logged-in user as sender
        user = self.scope.get("user")
        if not user or isinstance(user, AnonymousUser):
            # Not authenticated – don't allow sending messages
            await self.close()
            return

        sender_id = user.id

        # Assume chat_id in URL is the receiver's user id
        try:
            receiver_id = int(self.chat_id)
        except (TypeError, ValueError):
            # Bad URL / chat_id – bail out
            return

        # Save the message in the DB (runs in a thread)
        msg = await create_message(sender_id, receiver_id, content)

        # Broadcast to everyone in the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "message_id": msg.id,
                "message": content,          # <-- name it "message" for JS
                "sender_id": sender_id,
                "receiver_id": receiver_id,
            },
        )

    async def chat_message(self, event):
        # Send JSON back to WebSocket client
        await self.send(
            text_data=json.dumps(
                {
                    "message_id": event["message_id"],
                    "message": event["message"],
                    "sender_id": event["sender_id"],
                    "receiver_id": event["receiver_id"],
                }
            )
        )


# Alias for your routing if you still use it
DMConsumer = ChatConsumer
