import os
from kivy.lang import Builder
from kivy.uix.button import Button

Builder.load_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Buttons.kv'))


class MenuButton(Button):
    pass


class GameButton(Button):
    def __init__(self, coords, **kwargs):
        super().__init__(**kwargs)
        self.coords = coords
