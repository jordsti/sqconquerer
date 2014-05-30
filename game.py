__author__ = 'JordSti'

from SqException import GameException
from generator import map_generator
from map import *
from units import *
from turn import *

import time
import random


def default_units():
    units = ["archer", "warrior"]
    return units


class game_end_condition:

    def __init__(self, game, text="Nothing"):
        self.game = game
        self.text = text

    def is_ended(self):
        return False


class max_turn_condition(game_end_condition):

    def __init__(self, game, max_turns = 100):
        game_end_condition.__init__(self, game, "Ended by turns limit, %d turns" % max_turns)
        self.max_turns = max_turns

    def is_ended(self):
        if self.game.turns >= self.max_turns:
            return True
        else:
            return False


class game_context:
    def __init__(self, map_type='generated'):
        self.map = None
        self.filename = None
        self.width = 40
        self.height = 40
        self.map_type = map_type
        self.difficulty = 1
        self.end_conditions = []

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
        self.map = context.get_map()
        self.end_conditions = context.end_conditions
        self.spawnpoints = []

        self.current_player = None
        self.current_turn = None
        self.current_player_index = 0
        self.turn_constraints = []
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

    def generate_spawnpoints(self, min_distance=12):

        if not self.phase == self.Preparation:
            raise GameException(000003, "Invalid Phase")

        if len(self.spawnpoints) == 0:

            while len(self.spawnpoints) < len(self.players):
                x = random.randint(0, self.map.width - 1)
                y = random.randint(0, self.map.height - 1)

                t = self.map.get_tile(x, y)

                if t.tile_type == tile.Normal:
                    pt = coord(x, y)

                    for sp in self.spawnpoints:
                        if pt.distance_with(sp) < min_distance:
                            continue

                    self.spawnpoints.append(pt)

                else:
                    continue

    def next_turn(self):

        self.current_player_index += 1

        if self.current_player_index >= len(self.players):
            self.current_player_index %= len(self.players)

        self.current_player = self.players[self.current_player_index]

        if self.current_player == self.starting_player:
            self.turns += 1


    def assign_spawnpoint(self):
        for p in self.players:
            #picking random spawn point
            if len(self.spawnpoints) == 0:
                raise GameException(000004, "No more spawnpoint")

            pid = random.randint(0, len(self.spawnpoints) - 1)
            sp = self.spawnpoints[pid]
            p.spawnpoint = sp
            self.spawnpoints.remove(sp)

    def place_units(self, starting_unit=default_units()):
        for p in self.players:
            for u in starting_unit:
                unit_placed = False
                unit = create_unit(u, p)
                t = self.map.get_tile(p.spawnpoint.x, p.spawnpoint.y)
                pos = p.spawnpoint

                while not unit_placed:
                    if t.unit is None and t.walkable():
                        t.unit = unit
                        unit.assign_position(pos.x, pos.y)
                        unit_placed = True
                    else:
                        dx = random.randint(0, 4) - 2
                        dy = random.randint(0, 4) - 2
                        pos = coord(p.spawnpoint.x + dx, p.spawnpoint.x + dy)
                        t = self.map.get_tile(pos.x, pos.y)

    def start_game(self):
        if self.phase == self.Preparation:
            if len(self.players) >= 2:
                self.generate_spawnpoints()
                print "Spawnpoint created"
                self.assign_spawnpoint()
                print "Assigning spawnpoint"
                self.place_units()
                print "Unit placed"

                #debug purpose
                print self.map.to_string()

                self.phase = self.GameTurns

                ended = False

                for ec in self.end_conditions:
                    if ec.is_ended():
                        ended = True

                while not ended:
                    self.current_turn = turn_context(self, self.current_player)

                    while self.current_turn.ended:
                        self.current_turn.generate_units_view()

                        #get unit move


                        time.sleep(0.2)

                    #next playing

                    self.next_turn()

                    for ec in self.end_conditions:
                        if ec.is_ended():
                            print "Game added" #todo
                            break
            else:
                raise GameException(000002, "You need at least 2 players to start a game")
