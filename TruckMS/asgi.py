"""
ASGI config for TruckMS project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os # import os module for environment variable handling
from django.core.asgi import get_asgi_application # Import Django's ASGI application handler
from channels.routing import ProtocolTypeRouter, URLRouter # Import channels routing utilities
from channels.auth import AuthMiddlewareStack # Import authentication middleware for WebSocket connections
import fleetApp.routing # Import routing configuration from trucks app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TruckMS.settings') # Set default settings module for Django

application = ProtocolTypeRouter({   # Define the ASGI application for handling HTTP and WebSocket protocols
    'http': get_asgi_application(), # Route HTTP requests to Django's ASGI application
    'websocket': AuthMiddlewareStack(  # Route WebSocket requests through authentication middleware
        URLRouter(
            fleetApp.routing.websocket_urlpatterns #use the WebSocket URL patterns defined in the fleets app
        )
    ),
})