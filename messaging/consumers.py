#used chatgpt version 5 to generate and modify this code 
#used https://medium.com/@farad.dev/how-to-build-a-real-time-chat-app-using-django-channels-2ba2621ea972

# messaging/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import Message, Thread


@database_sync_to_async
def create_message(thread_id: int, sender_id: int, text: str) -> Message:
    # Adjust field names to match your Message model:
    # Message(thread=FK, sender=FK, text=TextField/CharField)
    return Message.objects.create(
        thread_id=thread_id,
        sender_id=sender_id,
        text=text,
    )

@database_sync_to_async
def thread_exists(thread_id: int) -> bool:
    return Thread.objects.filter(id=thread_id).exists()

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
        # chat_id is the thread id (see chat.html)
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_group_name = f"thread_{self.chat_id}"

        # (Optional) validate the thread exists; close if not
        try:
            valid = await thread_exists(int(self.chat_id))
        except ValueError:
            valid = False
        if not valid:
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return

        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return

        # Support both keys, default to "message" as your JS sends
        content = (data.get("message") or data.get("content") or "").strip()
        if not content:
            return

        user = self.scope.get("user")
        if not user or isinstance(user, AnonymousUser):
            await self.close()
            return

        sender_id = user.id
        try:
            thread_id = int(self.chat_id)
        except (TypeError, ValueError):
            return

        # Save to DB
        msg = await create_message(thread_id, sender_id, content)

        # Fan out to room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "message_id": msg.id,
                "message": content,
                "sender_id": sender_id,
                "thread_id": thread_id,
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message_id": event["message_id"],
            "message": event["message"],
            "sender_id": event["sender_id"],
            "thread_id": event["thread_id"],
        }))# Alias for your routing if you still use it
        
DMConsumer = ChatConsumer
