

class BasePlayer:
    def __init__(self, name: str):
        self.name = name
        self.points = 0

    def __iadd__(self, other: int):
        self.points += other
        self.on_add(other)
        return self

    def __isub__(self, other: int):
        self.points -= other
        self.on_sub(other)
        return self

    def on_add(self, other: int):
        pass

    def on_sub(self, other: int):
        pass
