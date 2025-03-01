import pygame
from src.constants import *


class Ship(pygame.sprite.Sprite):
    """ The class for displaying the ship object """

    # TODO  Make the x position change smoother

    def __init__(self, x, y, surface_group, object_group, obstacle_speed, skin_path):
        super().__init__(object_group)
        self.image = pygame.image.load(skin_path)
        self.rect = self.image.get_rect(topleft=(x, y))
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

    def game_over(self):
        global in_game
        in_game = False
        self.reset_position()

    def reset_position(self):
        self.rect.x = self.initial_x
        self.rect.y = self.initial_y
        self.current_angle = 0

    def update(self):
        keys = pygame.key.get_pressed()
        self.is_moving_up = keys[pygame.K_SPACE]

        if self.is_moving_up:
            self.target_angle = min(self.current_angle + ROTATION_SPEED, MAX_UPWARD_ROTATION)
            self.velocity_y = -self.speed_up
        else:
            self.target_angle = max(self.current_angle - ROTATION_SPEED, MAX_DOWNWARD_ROTATION)
            self.velocity_y = self.speed_down

        for surface in self.surface_group:
            if self.rect.colliderect(surface.rect):
                self.game_over()
                break

        self.rect.y += self.velocity_y
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

        self.current_angle = self.target_angle
        self.image = pygame.transform.rotate(self.original_image, self.current_angle)
        self.rect = self.image.get_rect(center=self.rect.center)
