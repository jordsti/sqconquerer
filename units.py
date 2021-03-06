__author__ = 'JordSti'

from map import coord
import math
import re
from player import dummy_player
from SqException import ParsingException


class unit:

    def __init__(self, name, owner, hp=5, power=1, move_range=1, view_range=2):
        self.position = coord()
        self.name = name
        self.move_range = move_range
        self.view_range = view_range
        self.max_hp = hp
        self.hp = hp
        self.power = power
        self.owner = owner

    def assign_position(self, x, y):
        self.position.x = x
        self.position.y = y

    def move(self, diff_x, diff_y):

        dx = math.fabs(diff_x)
        dy = math.fabs(diff_y)

        if dx + dy < self.move_range:
            self.position.x = self.position.x + diff_x
            self.position.y = self.position.y + diff_y

    def attack(self, target):
        target.defend(self, self.power)
        return

    def defend(self, source, power):
        self.hp = self.hp - power

        if self.hp <= 0:
            self.hp = 0

        return

    def is_dead(self):

        if self.hp == 0:
            return True
        else:
            return False

    def to_string(self):
        return "%s,%d/%d,%d" % (self.name, self.hp, self.max_hp, self.owner.player_id)

    def from_string(self, text):
        pattern = re.compile("(<name>[a-z]+),(<hp>[0-9]+)/(<max_hp>[0-9]+),(<id>[0-9]+)")

        m = pattern.match(text)

        if m:
            self.name = m.group("name")
            self.hp = int(m.group("hp"))
            self.max_hp = int(m.group("max_hp"))
            self.owner = dummy_player(int(m.group("id")))
        else:
            raise ParsingException(200001, "Unit parsing error")


class archer(unit):

    def __init__(self, owner):
        unit.__init__(self, "archer", owner, 4, 2, 2, 3)


class warrior(unit):

    def __init__(self, owner):
        unit.__init__(self, "warrior", owner, 6, 2, 1, 2)


def create_unit(name, owner):
    if name == 'archer':
        return archer(owner)
    elif name == 'warrior':
        return warrior(owner)
    else:
        return None


class unit_view:

    def __init__(self, unit):
        self.unit = unit
        self.tiles = {}

    def get_tiles(self, map):
        center_coord = self.unit.position

        view_range = self.unit.view_range

        for iy in range(view_range*2 + 1):
            y = iy - view_range
            if not y == 0:
                for ix in range(view_range*2 + 1):
                    x = ix - view_range
                    if not x == 0:
                        tx = (center_coord.x + x) % map.width
                        ty = (center_coord.y + y) % map.height

                        t = map.get_tile(tx, ty)
                        tc = coord(tx, ty)

                        self.tiles[tc] = t

    def contains_tiles_view(self, coord):

        for k in self.tiles:
            if k.x == coord.x and k.y == coord.y:
                return True

        return False


