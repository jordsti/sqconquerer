__author__ = 'JordSti'
import os
import random
import re
import math

from SqException import ParsingException

class coord:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def distance_with(self, coord2):

        dist = math.pow(coord2.x - self.x, 2) + math.pow(coord2.y - self.y, 2)

        return math.sqrt(dist)

    def diff(self, coord2):
        dx = math.fabs(coord2.x - self.x)
        dy = math.fabs(coord2.y - self.y)
        return dx, dy

    def from_string(self, text):

        pattern = re.compile("\\[(<x>[0-9]+),(<y>[0-9]+)\\]")
        m = pattern.match(text)

        if m:
            self.x = int(m.group("x"))
            self.y = int(m.group("y"))
        else:
            raise ParsingException(200005, "Invalid coord")

    def to_string(self):
        return "[%d,%d]" % (self.x, self.y)


class resource:

    def __init__(self, name, value=0):
        self.name = name
        self.value = value

    def to_string(self):
        return "%s-%d" % (self.name, self.value)


class resources:

    def __init__(self, filename='.resources'):
        self.filename = filename
        self.resources = []

        self.__load()

    def rand_res(self):
        rid = random.randint(0, len(self.resources)-1)

        return self.resources[rid]

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

        fp = open(self.filename, 'w')

        fp.write("copper:1\n")
        fp.write("iron:2\n")
        fp.write("gold:3\n")
        fp.write("horse:2\n")
        fp.write("cattle:1\n")

        fp.close()

        self.__load()


class tile:
    (Normal, Mountain, Water) = (0, 1, 2)

    def __init__(self, tile_type=Normal):
        self.tile_type = tile_type
        self.resources = []
        self.unit = None

    def walkable(self):
        return self.tile_type == self.Normal

    def from_string(self, text):

        pattern = re.compile("([0-9]+):([a-z,0-9\\-]*):([a-z:0-9/]*)")

        m = pattern.match(text)

        if m:
            type_id = int(m.group(1))
            res = m.group(2)
            ustr = m.group(3)

            if type_id == self.Normal or type_id == self.Mountain or type_id == self.Water:
                self.tile_type = type_id

            res = res.split(',')

            if not len(res) == 0:
                for r in res:
                    rpattern = re.compile("([a-z]+)\\-([0-9]+)")
                    m = rpattern.match(r)

                    if m:
                        rname = m.group(1)
                        rval = int(m.group(2))
                        self.resources.append(resource(rname, rval))


    def to_string(self):
        res = ""
        for r in self.resources:
            res += "%s-%d," % (r.name, r.value)

        ustr = ""

        if self.unit is not None:
            ustr = self.unit.to_string()

        res = res.rstrip(',')
        return "%d:%s:%s" % (self.tile_type, res, ustr)


class player_tile(tile):

    def __init__(self, tile_type=tile.Normal):
        tile.__init__(self, tile_type)

        self.visited = False
        self.last_visit = None

    def to_string(self):

        if not self.visited:
            return "x"
        else:
            return tile.to_string(self)

    def from_string(self, text):

        if text == 'x':
            self.tile_type = tile.Normal
            self.visited = False
            self.last_visit = None
            self.resources = []
            self.unit = None
        else:
            tile.from_string(self, text)

class game_map:

    def __init__(self, width=40, height=40, create_tile=True):
        self.width = width
        self.height = height

        self.tiles = []

        if create_tile:
            self.__init_map()

    def __init_map(self):
        for i in range(self.height):
            row = []
            self.tiles.append(row)

            for j in range(self.width):
                t = tile()
                row.append(t)

    def save(self, filename):
        fp = open(filename, 'w')

        data = self.to_string()

        fp.write(data)

        fp.close()

    def get_tile(self, x, y):

        if x < self.width and y < self.height:
            return self.tiles[y][x]

    def to_string(self):

        map_text = "map[%d][%d].start\n" % (self.width, self.height)

        for y in range(self.height):
            line = ""
            for x in range(self.width):
                t = self.get_tile(x, y)
                line = line + t.to_string() + "\t"

            line = line.rstrip('\t')

            map_text = map_text + line + '\n'

        map_text += "map.end\n"

        return map_text

    def from_string(self, text):

        self.tiles = []

        lines = text.split('\n')

        pattern = re.compile("map\\[([0-9]+)\\]\\[([0-9]+)\\]\\.start")

        m = pattern.match(lines[0])

        if m:
            width = int(m.group(1))
            height = int(m.group(2))

            self.width = width
            self.height = height

            self.__init_map()

            maps = lines[1:len(lines)-2]

            y = 0

            for row in maps:
                tiles = row.split('\t')
                x = 0
                for t in tiles:

                    mt = self.get_tile(x, y)
                    mt.from_string(t)
                    x += 1

                y += 1

class player_map(game_map):

    def __init__(self, width=40, height=40):
        game_map.__init__(self, width, height, False)

        self.__init_tiles()

    def __init_tiles(self):
        self.tiles = []

        for y in range(self.height):
            row = []
            self.tiles.append(row)
            for x in range(self.width):
                t = player_tile()
                row.append(t)

    def update_tile(self, x, y, tile_text):
        if x < self.width and y < self.height:
            t = self.get_tile(x, y)
            t.from_string(tile_text)



def load_map(filename):

    fp = open(filename, 'r')

    chunk = fp.read(1024)
    data = ""

    while len(chunk) > 0:
        data += chunk
        chunk = fp.read(1024)

    fp.close()

    gmap = game_map()
    gmap.from_string(data)

    return gmap
