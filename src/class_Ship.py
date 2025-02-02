import pygame
from math import sqrt, log, sin
from class_Surface import Surface
from constants import (PROJECT_PATH, FALL_STRENGTH, ROTATION_SPEED, MAX_UPWARD_ROTATION, MAX_DOWNWARD_ROTATION,
                       HEIGHT, GameObject)


class Ship(GameObject):
    """
    Корабль (лодка).
    Грамотно прописана система лавирования (верх / низ), но по возможности можно сделать ее плавнее.
    """

    def __init__(self, x, y, surface_group, object_group, skin, obstacle_speed):
        super().__init__(f"{PROJECT_PATH}\\assets\\images\\main_player\\player_ship.png", x, y, object_group)
        self.initial_x = x
        self.initial_y = y
        self.speed_up = 3
        self.speed_down = FALL_STRENGTH
        self.is_moving_up = False
        self.current_angle = 0
        self.target_angle = 0
        self.velocity_y = 0
        self.original_image = self.image
        self.surface_group = surface_group
        self.obstacle_speed = obstacle_speed
        self.skin = skin
        self.in_game = True
        self.current_move = 0
        self.max_bottom = HEIGHT
        self.min_top = 0

    def reset_position(self):
        self.rect.x = self.initial_x
        self.rect.y = self.initial_y
        self.current_angle = 0

    def update(self):
        keys = pygame.key.get_pressed()
        self.is_moving_up = keys[pygame.K_SPACE]

        if self.is_moving_up  and self.current_move < 15:
            self.current_move += 1
        elif not self.is_moving_up and self.current_move > -15:
            self.current_move -= 1

        k = -1 if self.current_move > 0 else 1
        self.velocity_y = (abs(self.current_move) / 3) ** log(5, 5) * k
        self.current_angle = (abs(self.current_move) / 3) ** log(45, 5) * k
        self.image = pygame.transform.rotate(self.original_image, -self.current_angle)
        self.rect.y += self.velocity_y
        if self.rect.bottom >= self.max_bottom:
            self.rect.bottom = self.max_bottom
        elif self.rect.top <= self.min_top:
            self.rect.top = self.min_top
        self.is_on_surface()
        self.rect = self.image.get_rect(center=self.rect.center)

    def is_on_surface(self): # Проверка на соприкосновение с платформой\дном
        for surface in self.surface_group:
            if self.rect.colliderect(surface.rect):
                if surface.is_dangerous():
                    self.in_game = False
                    break
                elif abs(self.rect.bottom - surface.rect.top) > 100 or abs(surface.rect.bottom - self.rect.top) > 100:
                    break
                else:
                    if abs(self.rect.bottom - surface.rect.top) <= 100:
                        self.max_bottom = surface.rect.top + 1
                        self.min_top = 0
                        self.rect.bottom = surface.rect.top
                        #self.current_move = 0
                        #self.current_angle = 0
                        break
                    elif abs(surface.rect.bottom - self.rect.top) <= 100:
                        self.min_top = surface.rect.bottom - 1
                        self.max_bottom = HEIGHT
                        self.rect.top = surface.rect.bottom - 1
                        self.current_move = 0
                        self.current_angle = 0
                        break

        else:
            self.max_bottom = HEIGHT
            self.min_top = 0
            print('------')
