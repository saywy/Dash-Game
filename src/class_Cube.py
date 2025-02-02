import pygame
from constants import (HEIGHT, JUMP_STRENGTH, PROJECT_PATH, ROTATION_SPEED, GRAVITY, GameObject)

SKIN = f"{PROJECT_PATH}\\assets\\images\\main_player\\player_cube.png"

class Cube(GameObject):
    """  Баг - возможен двойной прыжок"""
    def __init__(self, x, y, surface_group, object_group, skin):
        super().__init__(skin, x, y, object_group)
        self.velocity_y = 0
        self.is_jumping = False
        self.rotation_angle = 0
        self.surface_group = surface_group
        self.last_bottom = self.rect.bottom
        self.last_surface_top = HEIGHT
        self.skin = skin

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
                elif self.rect.bottom - surface.rect.top > 20:
                    return 'BAD'
                if self.velocity_y > 0:
                    self.rect.bottom = surface.rect.top
                    self.is_jumping = False
                    self.velocity_y = 0
                    self.last_surface_top = surface.rect.top
                    return True
        self.last_surface_top = HEIGHT + 100

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

        if abs(self.rect.bottom - self.last_bottom) < 5 or abs(HEIGHT - self.rect.bottom) < 5:
            by_module_90 = self.rotation_angle % 90
            if by_module_90 >= 45:
                self.rotation_angle += ROTATION_SPEED
            elif ROTATION_SPEED <= by_module_90 < 45:
                self.rotation_angle -= ROTATION_SPEED
            elif by_module_90 < ROTATION_SPEED:
                self.rotation_angle = self.rotation_angle // 90 * 90
        else:
            self.rotation_angle += ROTATION_SPEED
            self.rotation_angle %= 360
            self.last_bottom = self.rect.bottom

        self.update_image()
