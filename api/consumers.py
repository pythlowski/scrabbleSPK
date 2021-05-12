from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .game_logic import *
import json
import random


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

        async_to_sync(self.channel_layer.group_add)(
            f'group_{self.room_code}_{self.username}',
            self.channel_name
        )
        
        self.accept()

        is_host = False

        if self.room_code not in memory.keys():
            is_host = True
            memory[self.room_code] = {
                'started': False,
                'host': self.username,
                'grid': [[''] * 15 for i in range(15)],
                'bag': init_bag(),
                'players': [],
                'current_turn': 0
            }
            print(len(memory[self.room_code]['bag']))

        self.send(text_data=json.dumps({
                'message': 'init',
                'grid': memory[self.room_code]['grid'],
                'players': [{'username': player['username'], 'points': player['points'], 'theirTurn': player['theirTurn'], 'isHost': player['isHost']} for player in memory[self.room_code]['players']],
                'isHost': is_host,
                'yourUsername': self.username,
                'inBag': len(memory[self.room_code]['bag'])
            }))

        memory[self.room_code]['players'].append({
            'username': self.username,
            'seven_letters': [''] * 7,
            'points': 0,
            'theirTurn': False,
            'isHost': is_host
        })

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'new.player.message',
                'message': 'new_player',
                'username': self.username,
                'isHost': is_host
            }
        )


    def receive(self, text_data=None, bytes_bata=None):
        data = json.loads(text_data)
        if data['message'] == 'letters':
            self.send(text_data=json.dumps({
                'response': 'dzieki za litery'
            }))

            print(data['letters'])

            points = find_every_word_horizontally_and_vertically_and_calculate_points_for_every_founded_word_then_sum_it_all_for_pawel(
                memory[self.room_code]['grid'], data['letters']
            )
            # points = 10
            print(points)
            for letter in data['letters']:
                memory[self.room_code]['grid'][letter['y']][letter['x']] = letter['letter']

            for player in memory[self.room_code]['players']:
                if player['username'] == self.username:
                   player['points'] += points
            
            if memory[self.room_code]['current_turn'] + 1 == len(memory[self.room_code]['players']):
                memory[self.room_code]['current_turn'] = 0
            else:
                memory[self.room_code]['current_turn'] += 1

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

            from_bag = get_n_letters(len(data['letters']), memory[self.room_code]['bag'])
            self.send_letters_from_bag(self.username, from_bag)
            print(from_bag)

            added_letters = [x['letter'] for x in data['letters']]
            player = list(filter(lambda x: x['username'] == self.username, memory[self.room_code]['players']))[0]
            for i in range(7):
                if player['seven_letters'][i] in added_letters:
                    added_letters.remove(player['seven_letters'][i])
                    player['seven_letters'][i] = from_bag.pop(0) 
            print(memory[self.room_code]['players'])

            async_to_sync(self.channel_layer.group_send)(
                        self.group_name,
                        {
                            'type': 'turn.change.message',
                            'message': 'turn_change',
                            'username': memory[self.room_code]['players'][memory[self.room_code]['current_turn']]['username']
                        }
                    )

        elif data['message'] == 'game_start':
            if self.username == memory[self.room_code]['host']:
                self.send(text_data=json.dumps({
                    'response': 'juz zaczynam ale potwierdzone'
                }))
                memory[self.room_code]['started'] = True
                async_to_sync(self.channel_layer.group_send)(
                        self.group_name,
                        {
                            'type': 'game.start.message',
                            'message': 'game_start'
                        }
                    )

                for player in memory[self.room_code]['players']:
                    from_bag = get_n_letters(7, memory[self.room_code]['bag'])
                    player['seven_letters'] = from_bag 
                    self.send_letters_from_bag(player['username'], from_bag)

                async_to_sync(self.channel_layer.group_send)(
                        self.group_name,
                        {
                            'type': 'turn.change.message',
                            'message': 'turn_change',
                            'username': memory[self.room_code]['host']
                        }
                    )

    def new_player_message(self, event):

        self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
            'isHost': event['isHost']
        }))

    def new_letters_message(self, event):

        self.send(text_data=json.dumps({
            'message': event['message'],            
            'username': event['username'],
            'points': event['points'],
            'letters': event['letters'],
        }))

    def game_start_message(self, event):

        self.send(text_data=json.dumps({
            'message': event['message']
        }))

    def turn_change_message(self, event):

        self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username']
        }))

    def send_letters_from_bag(self, username, letters):
        group_name = f'group_{self.room_code}_{username}'
        async_to_sync(self.channel_layer.group_send)(
            group_name,
            {
                'type': 'from.bag.message',
                'message': 'from_bag',
                'letters': letters
            }
        )

    def from_bag_message(self, event):

        self.send(text_data=json.dumps({
            'message': event['message'],
            'letters': event['letters']
        }))

    def disconnect(self, close_code):
        pass