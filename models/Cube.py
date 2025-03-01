import pygame
from src.constants import *


class Cube(pygame.sprite.Sprite):
    """ Cube class   """

    # TODO Hanging in the air, double jump

    def __init__(self, x, y, surface_group, object_group, skin, obstacle_speed):
        super().__init__(object_group)
        self.image = pygame.image.load(skin)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity_y = 0
        self.is_jumping = False
        self.rotation_angle = 0
        self.surface_group = surface_group
        self.last_bottom = self.rect.bottom
        self.last_surface_top = HEIGHT
        self.skin = skin
        self.obstacle_speed = obstacle_speed

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = -JUMP_STRENGTH
            self.is_jumping = True

    @staticmethod
    def return_to_menu():
        return True

    def is_falling(self):
        self.rect.y += self.velocity_y
        for surface in self.surface_group:
            if self.rect.colliderect(surface.rect) or self.rect.bottom == surface.rect.top:
                if surface.is_dangerous():
                    return 'BAD'
                if self.velocity_y > 0:
                    self.rect.bottom = surface.rect.top
                    self.is_jumping = False
                    self.velocity_y = 0
                    return True
        return False

    def reset_position(self):
        self.rect.x = 100
        self.rect.bottom = self.last_bottom = HEIGHT
        self.velocity_y = 0
        self.is_jumping = False
        self.rotation_angle = 0

    def update_image(self):
        self.image = pygame.transform.rotate(
            pygame.image.load(self.skin),
            -self.rotation_angle
        )
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        if self.rect.y >= HEIGHT - self.rect.height:
            self.rect.y = HEIGHT - self.rect.height
            self.velocity_y = 0
            self.is_jumping = False

        self.is_falling()
        if self.rect.bottom == self.last_bottom or self.rect.bottom == HEIGHT:
            self.rotation_angle = 0
        else:
            self.rotation_angle += ROTATION_SPEED
            self.rotation_angle %= 360
            self.last_bottom = self.rect.bottom

        self.update_image()
