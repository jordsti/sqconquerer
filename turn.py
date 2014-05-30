__author__ = 'JordSti'

from SqException import UnitMoveException
from units import unit_view
import time

class turn_context:

    def __init__(self, game_object, player):
        self.game_object = game_object
        self.player = player
        self.units = []
        self.units_view = []
        self.ended = False
        self.started_at = time.time()

    def generate_units_view(self):

        for u in self.units:
            u_view = unit_view(u)
            u_view.get_tiles(self.game_object.map)
            self.units_view.append(u_view)

    def move_unit(self, unit, coords):

        if unit in self.units:
            #need to check new coord with dist and path

            if unit.move_range < len(coords):
                raise UnitMoveException(200003, "Too much move for this unit")

            last_case = unit.position
            for c in coords:
                (dx, dy) = last_case.diff(c)

                if dx <= 1 and dy <= 1:
                    t = self.game_object.map.get_tile(c.x, c.y)

                    if t.walkable() and t.unit is None:
                        #seems good
                        continue
                    elif t.walkable() and t.unit.owner.player_id == self.player.player_id:
                        continue
                    elif t.walkable() and t.unit is not None:
                        raise UnitMoveException(200002, "A unit from other player is in your way")
                    else:
                        raise UnitMoveException(200004, "This tile cannot be crossed")

                last_case = c

            end_tile = self.game_object.map.get_tile(last_case.x, last_case.y)
            end_tile.unit = unit
            unit.assign_position(last_case.x, last_case.y)
            self.units.remove(unit)
        else:
            raise UnitMoveException(200001, "You can't move this unit")


class turn_constraint:

    def __init__(self, turn, text="Nothing"):
        self.turn = turn
        self.text = text

    def is_ended(self):
        return False


class time_constraint(turn_constraint):

    def __init__(self, turn, limit=10):
        turn_constraint.__init__(self, turn, "Time limit hit %d seconds" % self.limit)
        self.limit = limit

    def is_ended(self):

        current = time.time()
        diff = current - self.turn.started_at

        if diff >= self.limit:
            return True

        return False