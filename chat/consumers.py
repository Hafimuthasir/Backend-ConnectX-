from channels.generic.websocket import WebsocketConsumer
from .models import Chat,Room
from asgiref.sync import async_to_sync
from djapp.models import User
import json
import django

django.setup()

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.roomid = self.scope['url_route']['kwargs']['roomid']
        self.sender = self.scope['url_route']['kwargs']['senderid']
        self.room_group_name = 'chat_%s' % self.roomid
        print(self.roomid)
        # Join the room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave the room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        # Save the message to the database
        obj = Room.objects.get(id=self.roomid)
        use = User.objects.get(id=self.sender)
        Chat.objects.create(
            owner=use,
            room=obj,
            messages=text_data
        )

        # Send the message to the room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'messages': text_data,
                'owner':self.sender,
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        # message = {'messages':event['messages'],'owner':self.sender}
        msg = json.dumps({
                'messages':event['messages'],
                'owner':self.sender 
        })
        # Send the message to the WebSocket
        self.send(text_data=msg)