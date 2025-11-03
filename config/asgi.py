"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # <-- set FIRST

from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()  # <-- initialize Django before importing your stuff

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import messaging.routing  # <-- safe to import now, after settings are ready

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(messaging.routing.websocket_urlpatterns)
    ),
})

