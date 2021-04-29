from channels.generic.websocket import WebsocketConsumer

from asgiref.sync import async_to_sync

import json


class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.group_name = f'group_{self.room_name}'

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'test.message',
                'content': 'siema'
            }
        )

    def test_message(self, event):

        self.send(text_data=json.dumps({
            'content': event['content']
        }))

    # def receive(self, json_data):
    #     data = json.loads(json_data)
    #     message = data['message']

    #     if message == 'letters':
    #         letters = message['letters']

    #         async_to_sync(self.channel_layer.group_send)(
    #         self.group_name,
    #         {
    #             'type': 'letters',
    #             'letters': letters
    #         }
    #     )

    # def letters(self, event):

    #     self.send(text_data=json.dumps({
    #         'letters': event['letters']
    #     }))