import pygame
import sys

class GameObject(pygame.sprite.Sprite):
    """ Parent class for all types of games """

    def __init__(self, image_path, x, y, group):
        super().__init__(group)
        try:
            self.image = pygame.image.load(image_path)
        except pygame.error as e:
            print(f"Error loading image {image_path}: {e}")
            sys.exit()
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)