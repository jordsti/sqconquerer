__author__ = 'JordSti'

from map import coord
import math


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
        return "%s:%d/%d:%d" % (self.name, self.hp, self.max_hp, self.owner)


class archer(unit):

    def __init__(self, owner):
        unit.__init__(self, "archer", owner, 4, 2, 2, 3)


class warrior(unit):

    def __init__(self, owner):
        unit.__init__(self, "warrior", owner, 6, 2, 1, 2)