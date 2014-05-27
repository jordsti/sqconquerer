__author__ = 'JordSti'
import os
import math


class coord:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def distance_with(self, coord2):

        dist = math.pow(coord2.x - self.x, 2) + math.pow(coord2.y - self.y, 2)

        return math.sqrt(dist)


class unit:

    def __init__(self, name, hp=5, power=1, move_range=1, view_range=2):
        self.position = coord()
        self.name = name
        self.move_range = move_range
        self.view_range = view_range
        self.hp = hp
        self.power = power


class resource:

    def __init__(self, name, value=0):
        self.name = name
        self.value = value


class resources:

    def __init__(self, filename='.resources'):
        self.filename = filename
        self.resources = []

        self.__load()

    def __load(self):
        if os.path.exists(self.filename):
            fp = open(self.filename, 'r')

            lines = fp.readlines()

            for l in lines:
                l = l.rstrip('\n').rstrip('\r')

                data = l.split(':')
                #data[0] -> name
                #data[1] -> value

                if len(data) == 2:
                    res = resource(data[0], int(data[1]))
                    self.resources.append(res)

            fp.close()
        else:

            self.__init_file()

    def __init_file(self):
        print "init that file"


class tile:
    (Normal, Mountain, Water) = (0, 1, 2)

    def __init__(self, tile_type=Normal):
        self.tile_type = tile_type
        self.resources = []
