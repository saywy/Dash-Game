import pygame
from constants import (PROJECT_PATH, HEIGHT, GameObject)
SKIN = f"{PROJECT_PATH}assets\\images\\main_player\\wave\\wave_straight.png"


class Wave(GameObject):
    """
    Волна (стрелочка). Баг - нет адекватной работы линии - траектории движения
    Сейчас переключается между 3-мя изображениями (с наклоном вверх / вниз / без наклона)
    Есть некая физика. При достижении верхней границы и зажатого пробела, отображение меняется на картинку без наклона
    Нужно поправить двойную подгрузку изображения без наклона
    """

    def __init__(self, x, y, surface_group, object_group, skin, obstacle_speed):
        super().__init__(f"{PROJECT_PATH}assets\\images\\main_player\\wave\\wave_straight.png", x, y, object_group)  # без наклона
        self.velocity_y = 0
        self.rect.x = x
        self.is_moving_up = False
        self.surface_group = surface_group
        self.object_group = object_group
        self.height = self.rect.bottom - self.rect.top
        self.skin = skin
        self.in_game = True
        self.obstacle_speed = obstacle_speed

    def update(self):
        keys = pygame.key.get_pressed()
        self.is_moving_up = keys[pygame.K_SPACE]
        for surface in self.surface_group:
            if self.rect.colliderect(surface.rect):
                self.in_game = False

        if self.is_moving_up:
            self.velocity_y = -self.obstacle_speed if self.rect.top > 0 else 0
        else:
            self.velocity_y = self.obstacle_speed if self.rect.bottom < HEIGHT else 0

        if self.is_moving_up and not self.rect.bottom - self.height <= 0:
            self.image = pygame.image.load(
                f"{PROJECT_PATH}\\assets\\images\\main_player\\wave\\wave_up.png")  # наклон вверх
        else:
            if self.rect.bottom >= HEIGHT or self.rect.bottom - self.height <= 0:
                self.image = pygame.image.load(
                    f"{PROJECT_PATH}\\assets\\images\\main_player\\wave\\wave_straight.png")  # без наклона
            else:
                self.image = pygame.image.load(
                    f"{PROJECT_PATH}\\assets\\images\\main_player\\wave\\wave_down.png")  # наклон вниз

        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.y += self.velocity_y

    def reset_position(self):
        self.rect.x = 200
        self.in_game = True
        self.velocity_y = 0
        self.is_moving_up = False