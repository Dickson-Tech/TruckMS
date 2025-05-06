import json # Import JSON for parsing websocket messages
from channels.generic.websocket import AsyncWebsocketConsumer # Import based webSocket consumer class
from .models import TruckLocation, Truck # Import models for database operations

# Define a WebSocket consumer for handling truck location updates
class TruckLocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.truck_id = self.scope['url_route']['kwargs']['truck_id'] # Extract truck ID from URL route
        self.truck_group_name = f'truck_{self.truck_id}' # Create a unique group name for the truck

        await self.channel_layer.group_add( # Add client to the truck group
            self.truck_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.truck_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        latitude = data['latitude']
        longitude = data['longitude']
        truck = Truck.objects.get(id=self.truck_id)

        # Save location to database
        TruckLocation.objects.create(
            truck=truck,
            latitude=latitude,
            longitude=longitude
        )

        # Broadcast location to group
        await self.channel_layer.group_send(
            self.truck_group_name,
            {
                'type': 'location_update',
                'latitude': latitude,
                'longitude': longitude,
                'truck_id': self.truck_id
            }
        )

    async def location_update(self, event):
        await self.send(text_data=json.dumps({
            'latitude': event['latitude'],
            'longitude': event['longitude'],
            'truck_id': event['truck_id']
        }))