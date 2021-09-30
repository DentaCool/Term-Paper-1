from itertools import cycle

from game.components.fields.BaseField import BaseField
from game.components.players import BasePlayer


class BaseGameMode:
    Field = BaseField

    def __init__(self, rows: int, cols: int, min_point: int, max_point: int, players: list[BasePlayer], seed: int = None):
        self.rows = rows
        self.cols = cols
        self.players = players
        self.players_cycle = cycle(players)
        self.table = self.Field.generate_fields_table(rows, cols, min_point, max_point, seed)
        self.current_pos = (None, None)

    def check(self, coords: tuple):
        pass

    def do_move(self, coords: tuple):
        if self.check(coords):
            self.on_move()

    def on_move(self):
        pass

