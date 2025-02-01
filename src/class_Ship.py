import pygame
from constants import (PROJECT_PATH, FALL_STRENGTH, ROTATION_SPEED, MAX_UPWARD_ROTATION, MAX_DOWNWARD_ROTATION,
                  HEIGHT, GameObject)


class Ship(GameObject):
    """
    Корабль (лодка).
    Грамотно прописана система лавирования (верх / низ), но по возможности можно сделать ее плавнее.
    """

    def __init__(self, x, y, object_group):
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

        self.rect.y += self.velocity_y
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))
        self.current_angle = self.target_angle
        self.image = pygame.transform.rotate(self.original_image, self.current_angle)
        self.rect = self.image.get_rect(center=self.rect.center)
