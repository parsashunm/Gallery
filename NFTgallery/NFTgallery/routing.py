"""
ASGI config for NFTgallery project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from products.consumers import PriceConsumer
from products.routing import websocket_urlpatterns

os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NFTgallery.settings')

# application = get_asgi_application()

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(
        websocket_urlpatterns
    )
})
