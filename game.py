__author__ = 'JordSti'

from SqException import GameException
from generator import map_generator
from map import *
from units import *
import random

class map_unit:
    def __init__(self, unit, x, y):
        self.position = coord(x, y)
        self.unit = unit


class game_context:
    def __init__(self, map_type='generated'):
        self.map = None
        self.filename = None
        self.width = 40
        self.height = 40
        self.map_type = map_type
        self.difficulty = 1

    def get_map(self):
        if self.map_type == 'generated':
            gen = map_generator(self.width, self.height)
            gen.generate(self.difficulty)
            self.map = gen.map
        elif self.map_type == 'file' and self.filename is not None:
            self.map = load_map(self.filename)

        return self.map


class game_object:

    (Preparation, GameTurns, End) = (0, 1, 2)

    def __init__(self, context=game_context()):

        self.phase = self.Preparation
        self.map = None
        self.players = []
        self.turns = 0
        self.context = context

        self.current_player = None
        self.current_player_index = 0

        self.starting_player = 0

    def add_player(self, player):
        if self.phase == self.Preparation:
            if player not in self.players:
                self.players.append(player)
        else:
            raise GameException(000001, "Preparation phase is over, player cannot be add")

    def pick_first(self):
        sid = random.randint(0, len(self.players)-1)

        self.starting_player = self.players[sid]

        print "Starting player is %s" % self.starting_player.name

        self.current_player_index = sid
        self.current_player = self.starting_player



