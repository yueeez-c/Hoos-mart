#used chat gpt version 5 for this

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"^ws/dm/(?P<chat_id>\d+)/$", consumers.DMConsumer.as_asgi()),
]
