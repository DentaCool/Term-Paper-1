import pandas as pd
from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

from game.GameModes import ClassicGameMode
from game.components.players import BasePlayer
from ui.buttons import GameButton
from ui.labels import PlayerPointsLabel
from ui.utils import set_bg, rgb_to_kivy


class WinnerNameTextInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        # обиеження в 30 символів та запобігання заборонених символів
        substring = substring[:30 - len(self.text)].replace(',', '')
        return super().insert_text(substring, from_undo=from_undo)


class GameOverWidget(FloatLayout):
    def __init__(self, winner, **kwargs):
        self.winner = winner
        super().__init__(**kwargs)


class GameOverPopup(Popup):
    # Користувач повинен вийти використовуючи кнопку, а не ESC
    # Тому ми обмежуємо доступ до неї
    def on_open(self):
        app = App.get_running_app()
        app.root.current_screen.esc_enabled = False

    def on_dismiss(self):
        app = App.get_running_app()
        app.root.current_screen.esc_enabled = True


class GameWidget(FloatLayout):
    GameButton = GameButton

    def new_game(self):
        # Видаляємо поле гри
        self.clear_game()

        # Підключаємо логіку гри та Створюємо поле гои
        self.game = ClassicGameMode(
            10, 10, -50, 100, [BasePlayer("Перший гравець"), BasePlayer("Другий гравець")]
        )
        self.game_table = self._generate_game_table()

        # Будуємо UI

        players_points = BoxLayout(
            orientation="horizontal",
            size_hint=(0.4, 0.1),
            pos_hint={"x": 0.3, "y": 0.9},
        )
        self.results = (
            PlayerPointsLabel(self.game.players[0]),
            PlayerPointsLabel(self.game.players[1]),
        )
        [players_points.add_widget(x) for x in self.results]
        self.add_widget(players_points)

        self.table_grid = GridLayout(
            rows=self.game.rows,
            cols=self.game.cols,
            size_hint=(0.8, 0.8),
            pos_hint={"x": 0.1, "y": 0.1},
        )
        [
            [self.table_grid.add_widget(widget) for widget in row]
            for row in self.game_table
        ]
        self.add_widget(self.table_grid)

    def clear_game(self):
        [widget.clear_widgets() for widget in self.children]

    def game_over(self):
        winner = max(self.game.players, key=lambda player: player.points)
        GameOverPopup(
            size_hint=(None, None),
            size=(500, 300),
            title="Гру закінчено",
            content=GameOverWidget(
                f"Переміг {winner.name} з результатом: {winner.points}!"
            ),
            auto_dismiss=False,
        ).open()
        self.clear_game()

    def save_result(self, winner_name: str):
        with open('./data/leaderboard.csv', 'a') as fd:
            fd.write(f"\n{winner_name if winner_name else 'Анонімний Гравець'},{max(self.game.players, key=lambda player: player.points).points}")

    def _generate_game_table(self):
        return [
            [
                self.GameButton(
                    coords=(y, x),
                    on_press=self._on_press,
                    on_release=self._on_release,
                    text=str(abs(self.game.table[y][x].points)),
                    background_color=self.game.table[y][x].color,
                    border=[1, 0, 1, 1],
                )
                for x in range(self.game.rows)
            ]
            for y in range(self.game.cols)
        ]

    def _draw_current_buttons_and_player_hint(
        self, horizontal_color=(1, 1, 1, 0.8), vertical_color=(1, 1, 1, 0.8)
    ):
        button_table = pd.DataFrame(self.game_table)
        for row in button_table.values:
            for button in row:
                button.canvas.before.clear()
        for player in self.results:
            player.canvas.before.clear()
        if self.game.current_type == "v":
            for button in button_table[self.game.current_pos[1]]:
                set_bg(button, bg_color=horizontal_color)
            set_bg(self.results[0], bg_color=horizontal_color, image='./labels/score_bg.png')
        if self.game.current_type == "h":
            for button in button_table.iloc[self.game.current_pos[0]]:
                set_bg(button, bg_color=vertical_color)
            set_bg(self.results[1], bg_color=vertical_color, image='./labels/score_bg.png')

    def update_result_labels(self):
        for label in self.results:
            label.update_points()

    def _on_press(self, button: GameButton):
        result = self.game.do_move(button.coords)
        if result["Result"]:
            button.background_color = [0, 0, 0, 0]
            button.text = ""
            SoundLoader.load("./ui/sfx/buttonrollover.wav").play()
            self._draw_current_buttons_and_player_hint(
                rgb_to_kivy([132, 151, 181, 0.4]), rgb_to_kivy([157, 152, 174, 0.4])
            )
            self.update_result_labels()
            self.on_move(button)
            if result["GameOver"]:
                self.game_over()

    def on_move(self, button: GameButton):
        SoundLoader.load("./ui/sfx/buttonclickrelease.wav").play()

    def _on_release(self, button: GameButton):
        pass


if __name__ == "__main__":
    class BaseGameUI(App):
        def build(self):
            game = GameWidget()
            game.new_game()
            return game

    BaseGameUI().run()
