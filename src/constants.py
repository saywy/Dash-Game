import os
import sys
import pygame


WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAVITY = 0.5
JUMP_STRENGTH = 8.5
ROTATION_SPEED = 5
OBSTACLE_SPEED = 3
FALL_STRENGTH = 3
MAX_UPWARD_ROTATION = 20
MAX_DOWNWARD_ROTATION = -20
ROTATION_FALL_SPEED = 2
TRACE_COLOR = pygame.color.Color(53, 68, 61)
PROJECT_PATH = str(os.path.dirname(__file__))[:-3]


class GameObject(pygame.sprite.Sprite):
    """ Родительский класс для всех видов игры """

    def __init__(self, image_path, x, y, group):
        super().__init__(group)
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"File '{fullname}' not found")
        sys.exit()
    img = pygame.image.load(fullname)
    if colorkey:
        img.set_colorkey(colorkey)
    return img
