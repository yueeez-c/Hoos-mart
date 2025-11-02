#used chatgpt version 5 to generate and modify this code 
#used https://medium.com/@farad.dev/how-to-build-a-real-time-chat-app-using-django-channels-2ba2621ea972

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import Message

#a class that users get an instance of when they connect, disconnect, or recieve a 
#message 

class ChatConsumer(AsyncWebsocketConsumer):
    #function that is called when a user opens a chat 
    async def connect(self):
        # must be authenticated
        if not self.scope.get("user") or isinstance(self.scope["user"], AnonymousUser):
            await self.close()
            return
        
        #who the user wants to message
        self.other_user_id = self.scope["url_route"]["kwargs"]["other_user_id"]
        #current user
        self.user = self.scope["user"]
        #generating a "chat room" id using both users ids
        ids = sorted([str(self.user.id), str(self.other_user_id)])
        self.room_name = f"dm_{ids[0]}_{ids[1]}"
        self.room_group_name = f"chat_{self.room_name}"
        
        #adding the users websocket connction to this new room and waits for it to open and accept
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    #called when user logs out/closes bage
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    #when the frontend sends a message to that room rocket 
    async def receive(self, text_data):
        payload = json.loads(text_data or "{}")
        message = (payload.get("message") or "").strip()
        if not message:
            return

        # persist first (so failures don't echo ghost messages)
        await self._save_message(self.user.id, self.other_user_id, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat.message", "message": message, "sender": self.user.username}
        )
    #when someone in the room sends a message, the message is the event and both people recieve that event
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"message": event["message"], "sender": event["sender"]}))

    @database_sync_to_async
    def _save_message(self, sender_id, receiver_id, content):
        return Message.objects.create(sender_id=sender_id, receiver_id=receiver_id, content=content)