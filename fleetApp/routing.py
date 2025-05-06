from django.urls import re_path # Import re_path for rregex-based URL patterns
from . import consumers # Import consumwers model for WebSocket handling

# Define WebSocket URL patterns for the trucks app
websocket_urlpatterns = [
    re_path(r'ws/truck/(?P<truck_id>\d+)/$', consumers.TruckLocationConsumer.as_asgi()), # Route websocket connections to consumers
]