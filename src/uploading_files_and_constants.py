import pygame

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60


def load_player_image():
    player_image = pygame.image.load(
        "C:\\Users\\Ususl\\PycharmProjects\\Dash game\\assets\\images\\main_player\\player_cube.png") # свой путь к изображению с главным персонажем
    return player_image


player_image = load_player_image()
