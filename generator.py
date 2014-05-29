__author__ = 'JordSti'

from map import *
from random import randint

class map_generator:

    def __init__(self, width=40, height=40):
        self.ress = resources()

        self.width = width
        self.height = height

        self.map = game_map(width, height)

    def generate(self, difficulty=1):

        for y in range(self.height):
            for x in range(self.width):
                ti = randint(0, 10 + difficulty)
                t = self.map.get_tile(x, y)
                if ti == 1:
                    t.tile_type = tile.Mountain
                elif ti == 2:
                    t.tile_type = tile.Water
                elif ti == 3:
                    #add one resources
                    t.resources.append(self.ress.rand_res())
                elif ti == 4:
                    #two ressources
                    t.resources.append(self.ress.rand_res())
                    t.resources.append(self.ress.rand_res())

                elif ti == 8:
                    t.resources.append(self.ress.rand_res())
                    t.resources.append(self.ress.rand_res())
                    t.resources.append(self.ress.rand_res())

                if difficulty > 10 and len(t.resources) == 0:
                    if ti % 4 == 0 or ti % 5 == 0:
                        t.tile_type = tile.Mountain
                    elif ti % 3 == 0:
                        t.tile_type = tile.Water

