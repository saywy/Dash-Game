import pygame
from constants import (PROJECT_PATH, HEIGHT, GameObject)


class Wave(GameObject):
    """
    Волна (стрелочка). Баг - нет адекватной работы линии - траектории движения
    Сейчас переключается между 3-мя изображениями (с наклоном вверх / вниз / без наклона)
    Есть некая физика. При достижении верхней границы и зажатого пробела, отображение меняется на картинку без наклона
    Нужно поправить двойную подгрузку изображения без наклона
    """

    def __init__(self, x, y):
        super().__init__(f"{PROJECT_PATH}assets\\images\\main_player\\wave\\wave_straight.png", x, y)  # без наклона
        self.velocity_y = 0
        self.is_moving_up = False

    def update(self):
        keys = pygame.key.get_pressed()
        self.is_moving_up = keys[pygame.K_SPACE]

        if self.is_moving_up:
            self.velocity_y = -5 if self.rect.top > 0 else 0
        else:
            self.velocity_y = 5 if self.rect.bottom < HEIGHT else 0

        if self.is_moving_up:
            self.image = pygame.image.load(
                f"{PROJECT_PATH}\\assets\\images\\main_player\\wave\\wave_up.png")  # наклон вверх
        else:
            if self.rect.bottom >= HEIGHT:
                self.image = pygame.image.load(
                    f"{PROJECT_PATH}\\assets\\images\\main_player\\wave\\wave_straight.png")  # без наклона
            else:
                self.image = pygame.image.load(
                    f"{PROJECT_PATH}\\assets\\images\\main_player\\wave\\wave_down.png")  # наклон вниз

        self.rect = self.image.get_rect(center=self.rect.center)
