from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .game_logic import *
from .models import Room
import json
import random
import time


memory = {}

class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.group_name = f'group_{self.room_code}'
        self.username = self.scope['session']['nickname']
        self.room_model = Room.objects.get(code=self.room_code)


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
            limit = 4
            memory[self.room_code] = {
                'started': False,
                'host': self.username,
                'limit': self.room_model.max_players,
                'grid': [[''] * 15 for i in range(15)],
                'bag': init_bag(),
                'players': [],
                'current_turn': 0,
                'skipped_in_row': 0,
                'last_turn': {}
            }
            # print('Left in bag:', len(memory[self.room_code]['bag']))
        else:
            
            host = list(filter(lambda x: x['isHost'], memory[self.room_code]['players']))[0]['username']
            if host == self.username:
                is_host = True

        usernames = [player['username'] for player in memory[self.room_code]['players']]
        
        print(f'{self.username} trying to connect to the game...')
        if not memory[self.room_code]['started'] and (len(memory[self.room_code]['players']) < memory[self.room_code]['limit']) and (self.username not in usernames):

            memory[self.room_code]['players'].append({
                'username': self.username,
                'seven_letters': [''] * 7,
                'points': 0,
                'theirTurn': is_host,
                'isHost': is_host
            })
            self.room_model.current_players += 1

            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type': 'new.player.message',
                    'message': 'new_player',
                    'username': self.username,
                    'isHost': is_host
                }
            )

        seven_letters = [''] * 7
        if self.username in usernames:
            player = list(filter(lambda x: x['username'] == self.username, memory[self.room_code]['players']))[0]
            seven_letters = player['seven_letters'] if self.username in usernames else [''] * 7
        print('init, ktoremu wysylam takie 7 letters:', seven_letters)
        self.send(text_data=json.dumps({
                'message': 'init',
                'started': memory[self.room_code]['started'],
                'grid': memory[self.room_code]['grid'],
                'players': [{'username': player['username'], 'points': player['points'], 'theirTurn': player['theirTurn'], 'isHost': player['isHost']} for player in memory[self.room_code]['players']],
                'currentTurn': memory[self.room_code]['players'][memory[self.room_code]['current_turn']]['username'],
                'yourUsername': self.username,
                'isHost': is_host,
                'sevenLetters': seven_letters,
                'inBag': len(memory[self.room_code]['bag']),
            }))

        print([player['username'] for player in memory[self.room_code]['players']])

    def receive(self, text_data=None, bytes_bata=None):
        data = json.loads(text_data)
        if data['message'] == 'letters':
            
            memory[self.room_code]['skipped_in_row'] = 0

            self.send(text_data=json.dumps({
                'response': 'dzieki za litery'
            }))

            points, words = calculate_points(memory[self.room_code]['grid'], data['letters'])
            
            print(points, words)

            for letter in data['letters']:
                memory[self.room_code]['grid'][letter['y']][letter['x']] = letter['letter']

            for player in memory[self.room_code]['players']:
                if player['username'] == self.username:
                   player['points'] += points

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
            player = list(filter(lambda x: x['username'] == self.username, memory[self.room_code]['players']))[0]

            memory[self.room_code]['last_turn']['letters'] = data['letters']  
            memory[self.room_code]['last_turn']['words'] = words 
            memory[self.room_code]['last_turn']['player'] = {
                'username': self.username,
                'seven_letters': player['seven_letters'].copy(),
                'from_bag': from_bag.copy(),
                'points': points
            } 

            self.send_letters_from_bag(self.username, from_bag)

            added_letters = [x['letter'] if x['letter'][0] != 'b' else ' ' for x in data['letters']]
            
            for i in range(7):
                if player['seven_letters'][i] in added_letters:
                    added_letters.remove(player['seven_letters'][i])
                    if len(from_bag) > 0:
                        player['seven_letters'][i] = from_bag.pop(0) 
                    else:
                        player['seven_letters'][i] = ''

            if not list(filter(lambda x: x != '', player['seven_letters'])):
                print('Game over')
                self.game_over()
            else:
                self.switch_turn()

            
        elif data['message'] == 'game_start':

            memory[self.room_code]['skipped_in_row'] = 0
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

        elif data['message'] == 'turn_skip':
            memory[self.room_code]['skipped_in_row'] += 1
            print(memory[self.room_code]['skipped_in_row'])
            if memory[self.room_code]['skipped_in_row'] == 2 * len(memory[self.room_code]['players']):
                self.game_over()

            memory[self.room_code]['last_turn'] = {}   
            self.switch_turn()

        elif data['message'] == 'letters_exchange':

            memory[self.room_code]['skipped_in_row'] = 0

            letters_to_exchange = data['letters']
            print('I got', letters_to_exchange)
            to_exchange_count = len(letters_to_exchange)
            if  0 < to_exchange_count <= len(memory[self.room_code]['bag']):
                
                from_bag = get_n_letters(to_exchange_count, memory[self.room_code]['bag'])
                print('Sending', from_bag)
                self.send_letters_from_bag(self.username, from_bag)
                memory[self.room_code]['bag'] += letters_to_exchange
                random.shuffle(memory[self.room_code]['bag'])

                player = list(filter(lambda x: x['username'] == self.username, memory[self.room_code]['players']))[0]
                
                for i in range(7):
                    if player['seven_letters'][i] in letters_to_exchange:
                        letters_to_exchange.remove(player['seven_letters'][i])
                        if len(from_bag) > 0:
                            player['seven_letters'][i] = from_bag.pop(0) 
                        else:
                            player['seven_letters'][i] = ''
                            
            self.switch_turn()
        
        elif data['message'] == 'question_turn':
            if memory[self.room_code]['last_turn']:
                username = memory[self.room_code]['last_turn']['player']['username']
                words_checked = [(word, legal_word(word)) for word in memory[self.room_code]['last_turn']['words']]
                incorrect_words = [word for (word, is_legal) in words_checked if not is_legal]

                async_to_sync(self.channel_layer.group_send)(
                        self.group_name,
                        {
                            'type': 'turn.question.response',
                            'message': 'turn_question_response',
                            'incorrect_words': incorrect_words,
                            'username': username,
                            'letters_to_revert': memory[self.room_code]['last_turn']['letters'],
                            'points_to_revert': memory[self.room_code]['last_turn']['player']['points']
                        }
                    )
                if incorrect_words:
                    print('Reverting player\'s data')
                    
                    player = list(filter(lambda x: x['username'] == username, memory[self.room_code]['players']))[0]

                    player['seven_letters'] = memory[self.room_code]['last_turn']['player']['seven_letters']
                    player['points'] -= memory[self.room_code]['last_turn']['player']['points']

                    for letter in memory[self.room_code]['last_turn']['letters']:
                        memory[self.room_code]['grid'][letter['y']][letter['x']] = ''
                    memory[self.room_code]['bag'] += memory[self.room_code]['last_turn']['player']['from_bag']

                    # send reverted data to this player
                    group_name = f'group_{self.room_code}_{username}'
                    async_to_sync(self.channel_layer.group_send)(
                        group_name,
                        {
                            'type': 'revert.details.message',
                            'message': 'revert_details',
                            'new_seven_letters': player['seven_letters']
                        }
                    )

                    memory[self.room_code]['last_turn'] = {}

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

    def game_over_message(self, event):

        self.send(text_data=json.dumps({
            'message': event['message'],
            'winners': event['winners'],
            'points': event['points'],
        }))

    def turn_question_response(self, event):
        self.send(text_data=json.dumps({
            'message': event['message'],
            'incorrect_words': event['incorrect_words'],
            'username': event['username'],
            'letters_to_revert': event['letters_to_revert'],
            'points_to_revert': event['points_to_revert']
        }))

    def revert_details_message(self, event):
        self.send(text_data=json.dumps({
            'message': event['message'],
            'new_seven_letters': event['new_seven_letters']
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

    def switch_turn(self):
        memory[self.room_code]['players'][memory[self.room_code]['current_turn']]['theirTurn'] = False

        if memory[self.room_code]['current_turn'] + 1 == len(memory[self.room_code]['players']):
                memory[self.room_code]['current_turn'] = 0
        else:
            memory[self.room_code]['current_turn'] += 1

        memory[self.room_code]['players'][memory[self.room_code]['current_turn']]['theirTurn'] = True
        async_to_sync(self.channel_layer.group_send)(
                    self.group_name,
                    {
                        'type': 'turn.change.message',
                        'message': 'turn_change',
                        'username': memory[self.room_code]['players'][memory[self.room_code]['current_turn']]['username']
                    }
                )

    def game_over(self):
        players_sorted = sorted(memory[self.room_code]['players'], key=lambda x: x['points'], reverse=True)
        max_points  = players_sorted[0]['points']
        winners = list(filter(lambda x: x['points'] == max_points, players_sorted))
        del players_sorted

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'game.over.message',
                'message': 'game_over',
                'winners': [player['username'] for player in winners],
                'points': max_points,
            }
        )

    def from_bag_message(self, event):

        self.send(text_data=json.dumps({
            'message': event['message'],
            'letters': event['letters']
        }))

    def disconnect(self, close_code):
        pass