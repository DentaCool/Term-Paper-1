import csv

from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout

class LeaderBoardWidget(BoxLayout):
    rows = ListProperty([("name", "points")])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print(self.children)

    def load_data(self):
        with open("./data/leaderboard.csv") as datafile:
            self.rows = sorted(list(csv.reader(datafile)), key=lambda x: int(x[1]), reverse=True)[:6]