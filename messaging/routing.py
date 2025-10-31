#used chat gpt version 5 for this

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/dm/(?P<other_user_id>\w+)/$", consumers.ChatConsumer.as_asgi()),
]
