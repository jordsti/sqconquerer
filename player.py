__author__ = 'JordSti'

import time
import hashlib
import random
from map import coord

current_id = 1

def get_player_id():
    global current_id
    player_id = current_id
    current_id += 1

    return player_id

class dummy_player:
    def __init__(self, player_id):
        self.player_id = player_id

class game_player:
    def __init__(self, name):
        self.player_id = get_player_id()
        self.name = name
        self.spawnpoint = coord(0, 0)

class game_session:
    def __init__(self, player):
        self.player = player
        self.key = ""
        self.created_on = time.time()
        self.last_action = time.time()

        self.__generate_key()

    def tick(self):
        self.last_action = time.time()

    def get_socket(self):
        return self.player.client_socket

    def __generate_key(self):

        i1 = random.randint(0,10000)
        i2 = random.randint(10000,500000)

        text = "%s:%d:%d:%d" % (self.player.name, self.created_on, i1, i2)

        hasher = hashlib.sha256()

        hasher.update(text)

        self.key = hasher.hexdigest()


class net_player(game_player):

    def __init__(self, name, client_socket):
        game_player.__init__(self, name)
        self.client_socket = client_socket
        self.session = game_session(self)

    def get_key(self):
        return self.session.key

    def get_last_action(self):
        return self.session.last_action

    def get_created_on(self):
        return self.session.created_on



