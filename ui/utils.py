from kivy.graphics import *


def set_bg(layout, **options):
    with layout.canvas.before:
        if "bg_color" in options:
            Color(*options["bg_color"])
        layout.bg_rect = Rectangle(
            pos=layout.pos, size=layout.size,  source=options.get("image", None)
        )

        def update_rect(instance, value):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size

        # Змінюємо позицію разом з елементом (необхідно при зміні розміру вікна та позиції елементів)
        layout.bind(pos=update_rect, size=update_rect)


def rgb_to_kivy(color: list):
    return list(x/255 for x in color[:3]) + color[3:]
