#!/usr/bin/python
# -*- coding: UTF-8  -*-
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button

from ui.pages import LeaderBoardWidget
from ui.pages import GameWidget
from ui.utils import set_bg, rgb_to_kivy
# Задаємо початковий та мінімальний розмір вікна
Window.size = (800, 600)
Window.minimum_width, Window.minimum_height = Window.size


class HelpWidget(ScrollView):
    help_text = """
                                                           НАВІГАЦІЯ:
                                                           
    F1  - відкрити/закрити Посібник Користувача
    ESC - повернутися назад
    
    
    
                                                           ПРАВИЛА:

    ІГРОВЕ поле має розмір 10х10 клітинок, які складаються з випадково
розподілених чисел.

    ПЕРШИЙ гравець ходить по горизонталі і вибирає будь-яку клітинку на ній,
другий – по вертикалі.

    ЯКЩО колір вибраної клітинки червоний, то бали, вказані на ній,
додаються до рахунку гравця, якщо синій – віднімаються.

    ПІСЛЯ ходу першого гравця вертикаль, на якій знаходиться вибрана ним
клітинка, стає поточною і хід переходить до супротивника, який може 
вибрати будь-яку клітинку з цифрою на ній і т.д.

    ГРА завершується, коли оброблені всі клітинки, або неможливо 
здійснити хід.
    
    МЕТА гри – набрати більше балів, ніж суперник.
"""


class BackWidget(BoxLayout):
    pass


class HelpPopup(Popup):
    is_opened = False

    def on_open(self):
        self.is_opened = True

    def on_dismiss(self):
        self.is_opened = False


class BackPopup(Popup):
    is_opened = False

    def on_open(self):
        self.is_opened = True

    def on_dismiss(self):
        self.is_opened = False


class MainMenuScreen(Screen):
    back_popup = True
    esc_enabled = True

    def on_pre_enter(self, *args):
        set_bg(self, image="./ui/textures/default/background/menu.jpg")


class GameScreen(Screen):
    back_popup = True
    esc_enabled = True

    # Перед запуском гри, ми створюємо/видаляємо її віджети
    def on_pre_enter(self):
        set_bg(self, image="./ui/textures/default/background/menu.jpg")
        self.children[0].new_game()


class LeaderBoardScreen(Screen):
    esc_enabled = True

    def on_pre_enter(self, *args):
        set_bg(self, image="./ui/textures/default/background/menu.jpg")
        self.children[0].load_data()


class RootScreenManager(ScreenManager):
    def __init__(self, help_widget):
        super().__init__()
        self._help_widget = help_widget
        self.list_of_prev_screens = []

    def prev_screen(self):
        # Перевірте, чи є екрани, до яких можна повернутися
        if self.list_of_prev_screens:
            # Якщо є, то змінюємо сurrent на цей екран
            self.current = self.list_of_prev_screens.pop()
            return True
        # Якщо немає, значить мо хочемо вийти
        return exit()

    def next_screen(self, btn: Button, next_screen: str):
        # Додаємо екран, в якому ми щойно були
        self.list_of_prev_screens.append(btn.parent.parent.name)
        # Перейти до наступного екрана
        self.current = next_screen


class MainApp(App):
    esc_enabled = True
    cheat_code = [273, 273, 274, 274, 276, 275, 276, 275, 98, 97]  # Konami code
    cheat_stack = []

    def open_settings(self, *args):
        """
        Замінюємо налаштування kivy на наш help_popup
        """

        # F1 - Відрити\Закрити HelpWidget
        if self._help_widget.is_opened:
            self._help_widget.dismiss()
        else:
            self._help_widget.open()

    def _cheat_check(self, key):
        # якщо стек == код
        if self.cheat_code == self.cheat_stack:
            # та поточний екран є грою
            if self.root.current == "game_screen":
                # то додаємо +100 очків до поточного гравця
                if key == 273:
                    self.root.current_screen.children[0].game.current_player += 100
                # або ж віднімаємо 100
                elif key == 274:
                    self.root.current_screen.children[0].game.current_player -= 100
                else:
                    self.cheat_stack = []
                self.root.current_screen.children[0].update_result_labels()

        # добавляємо кнопки до стеку якщо код вводиться правильно
        if len(self.cheat_stack) < len(self.cheat_code):
            if self.cheat_code[len(self.cheat_stack)] == key:
                self.cheat_stack.append(key)
            # інакше видаляємо стек
            else:
                self.cheat_stack = []

    def _keyboard_hook(self, *touch):
        key = touch[1]
        self._cheat_check(key)
        if key == 27 and self.root.current_screen.esc_enabled:  # ESC - перехід на попередній екран\закрити Popup
            # Закриваємо help якщо він відкритий
            if self._help_widget.is_opened:
                self._help_widget.dismiss()
                return True
            # Перевіряємо чи наш екран потребує підтвердження для виходу (чи відкривати back_popup)
            if getattr(self.root.current_screen, "back_popup", False):
                # Закриваємо\Відкриваємо back_popup
                if self._back_popup.is_opened:
                    self._back_popup.dismiss()
                else:
                    self._back_popup.open()
                return True
            # в інших випадках повертаємось на минулий екран
            self.root.prev_screen()
        return True

    def build(self):
        self.title = "Решітка"
        # Будуємо наші Popup`s в App для зручного подальшого доступу та контролю
        self._help_widget = HelpPopup(
            title="Посібника Користувача",
            title_align='center',
            content=HelpWidget(),
            size_hint=(None, None),
            size=(600, 600),
        )
        self._back_popup = BackPopup(
            title="Вийти?",
            title_align='center',
            content=BackWidget(),
            size_hint=(None, None),
            size=(500, 300),  # (300, 200)
        )
        Window.bind(on_keyboard=self._keyboard_hook)  # ловимо всі натиски клавіатури/мишки на вікно програми
        return RootScreenManager(help_widget=self._help_widget)


if __name__ == "__main__":
    app = MainApp()
    app.destroy_settings()
    app.run()
