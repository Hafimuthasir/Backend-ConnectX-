import os
from django.core.asgi import get_asgi_application
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoproject.settings")
django_asgi_app = get_asgi_application()
django.setup()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from django.urls import path
from chat.consumers import *





application = ProtocolTypeRouter({
    "http": django_asgi_app,

    # WebSocket chat handler
    "websocket": 
        AuthMiddlewareStack(
            URLRouter([
               path('ws/chat/<int:roomid>/<int:senderid>/',ChatConsumer.as_asgi()),
            ])
        )

})