from . import BaseField


class ClassicField(BaseField):
    COLORS = {
        "blue": [0, 0, 1, 1],
        "red": [1, 0, 0, 1]
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = self.COLORS["red"] if self.points > 0 else self.COLORS["blue"]

    def __str__(self):
        return f"P: {self.points} C:{self.color}"
