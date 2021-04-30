from channels.generic.websocket import WebsocketConsumer

from asgiref.sync import async_to_sync

import json

memory = {}

class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.group_name = f'group_{self.room_code}'
        self.username = self.scope['session']['nickname']

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        
        self.accept()

        if self.room_code not in memory.keys():
            memory[self.room_code] = {
                'grid': [[''] * 15 for i in range(15)],
                'players': []
            }

        self.send(text_data=json.dumps({
                'message': 'init',
                'grid': memory[self.room_code]['grid'],
                'players': [{'username': player['username'], 'points': player['points']} for player in memory[self.room_code]['players']],
            }))

        memory[self.room_code]['players'].append({
            'username': self.username,
            'channel_name': self.channel_name,
            'seven_letters': [''] * 7,
            'points': 0
        })

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'new.player.message',
                'message': 'new_player',
                'username': self.username
            }
        )

    def new_player_message(self, event):

        self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username']
        }))

    def receive(self, text_data=None, bytes_bata=None):
        data = json.loads(text_data)
        if data['message'] == 'letters':
            self.send(text_data=json.dumps({
                'response': 'dzieki za litery'
            }))

            for letter in data['letters']:
                memory[self.room_code]['grid'][letter['y']][letter['x']] = letter['letter']

            points = 12
            for player in memory[self.room_code]['players']:
                if player['channel_name'] == self.channel_name:
                   player['points'] += points
            print(memory[self.room_code]['players'])

            async_to_sync(self.channel_layer.group_send)(
                    self.group_name,
                    {
                        'type': 'new.letters.message',
                        'message': 'letters',
                        'username': self.username,
                        'points': points,
                        'letters': data['letters'],
                    }
                )

    def new_letters_message(self, event):

        self.send(text_data=json.dumps({
            'message': event['message'],            
            'username': event['username'],
            'points': event['points'],
            'letters': event['letters'],
        }))

    def disconnect(self, close_code):
        pass