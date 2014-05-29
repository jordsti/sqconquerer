__author__ = 'JordSti'

from SqException import GameException
from generator import map_generator
from map import *
from units import *
import random


def default_units():
    units = ["archer", "warrior"]
    return units


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
        self.map = context.get_map()
        self.spawnpoints = []

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
            else:
                raise GameException(000002, "You need at least 2 players to start a game")
