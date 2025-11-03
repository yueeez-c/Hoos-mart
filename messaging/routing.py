# messaging/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # adjust the path to whatever your frontend uses
    re_path(r"^ws/dm/(?P<chat_id>\d+)/$", consumers.ChatConsumer.as_asgi()),
]
