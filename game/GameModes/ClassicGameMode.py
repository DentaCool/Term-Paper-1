from itertools import cycle

from game.components.fields.ClassicField import ClassicField
from . import BaseGameMode


class ClassicGameMode(BaseGameMode):
    Field = ClassicField
    move_type = cycle(("h", "v"))
    current_type = "h"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_player = next(self.players_cycle)
        self.CHECK_FUNC = {
            "h": self.horizontal_check,
            "v": self.vertical_check
        }

    def horizontal_check(self, coords: tuple):
        if self.current_pos[0] == coords[0] and self.table[coords[0]][coords[1]]:
            return {"STATUS": True}
        return {"STATUS": False}

    def vertical_check(self, coords: tuple):
        if self.current_pos[1] == coords[1] and self.table[coords[0]][coords[1]]:
            return {"STATUS": True}
        return {"STATUS": False}

    def game_over_check(self):
        if self.current_type == "h" and len(list(filter(lambda x: x is None, self.table[self.current_pos[0]]))) == self.cols:
            return True
        if self.current_type == "v" and len(list(filter(lambda x: x is None, self.table.iloc[self.current_pos[1]]))) == self.rows:
            return True

    def do_move(self, coords: tuple):
        if self.current_pos == (None, None):
            self.current_pos = coords
        if self.CHECK_FUNC[self.current_type](coords)["STATUS"]:
            self.current_player += self.table[coords[0]][coords[1]].points
            self.table[coords[0]][coords[1]] = None
            self.current_pos = coords
            self.current_player = next(self.players_cycle)
            self.current_type = next(self.move_type)
            return {"Result": True, "GameOver": self.game_over_check()}
        return {"Result": False, "GameOver": False}
