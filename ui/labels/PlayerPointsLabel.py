from kivy.uix.label import Label


class PlayerPointsLabel(Label):
    def __init__(self, player=None, **kwargs):
        super().__init__(**kwargs)
        self.player = player

    def update_points(self):
        self.text = f"{self.player.name}: {self.player.points}"
        self.on_update()

    def on_update(self):
        pass
