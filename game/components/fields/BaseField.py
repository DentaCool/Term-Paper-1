import pandas as pd
import random


class BaseField:
    def __init__(self, points: int):
        self.points = points

    def __repr__(self):
        return "{}".format([f'{x}: {self.__dict__[x]}' for x in self.__dict__])

    @classmethod
    def generate_fields_table(cls, width: int, height: int, min_value: int, max_value: int, seed: int = None):
        """
        Args:
            :param max_value: Максимальна кількість очків
            :param min_value: Мінімальна кількість очків
            :param height: Висота таблиці
            :param width: Ширина таблиці
            :param seed: Ключ для геренації
        """
        if isinstance(seed, int):
            random.seed(seed)
        return pd.DataFrame(((cls(random.randint(min_value, max_value)) for _ in range(width)) for _ in range(height)))
