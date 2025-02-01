import pygame
from constants import (PROJECT_PATH, OBSTACLE_SPEED, GameObject)


class Surface(GameObject):
    """ Платформа. баг - отображение нижней платформы (чуть выше чем нужно), может быть изменено при необходимости  """

    def __init__(self, x, y):
        super().__init__(f'{PROJECT_PATH}\\assets\\images\\cub.png', x, y)
        self.is_drawn = False

    @staticmethod
    def is_dangerous():
        return False

    def update(self):
        if not self.is_drawn:
            self.rect.x -= OBSTACLE_SPEED
        if self.rect.x < -self.rect.width:
            self.is_drawn = True
