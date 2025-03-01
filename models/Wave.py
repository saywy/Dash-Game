import pygame
from .GameObject import GameObject
from src.constants import *


class Wave(GameObject):
    """ The wave object in the game. """

    # TODO: Proper mapping of routes

    def __init__(self, x, y, surface_group, object_group, skin, obstacle_speed):
        super().__init__(skin, x, y, object_group)
        self.velocity_y = 0
        self.is_moving_up = False
        self.surface_group = surface_group
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

        if self.is_moving_up:
            self.image = pygame.image.load(f"{PROJECT_PATH}\\assets\\images\\main_player\\wave\\wave_up.png")
        else:
            self.image = pygame.image.load(f"{PROJECT_PATH}\\assets\\images\\main_player\\wave\\wave_straight.png")

        self.rect.y += self.velocity_y
