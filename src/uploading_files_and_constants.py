import pygame

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

FULL_SCREEN_WIDTH = 1920
FULL_SCREEN_HEIGHT = 1080

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
FPS = 60

font_Monaco_path = "C:\\Users\\Ususl\\PycharmProjects\\Dash game\\assets\\fonts\\Monaco.otf"  # пока что используется Absolute Path. Нужно поменять


def load_player_image():
    player_image = pygame.image.load(
        "C:\\Users\\Ususl\\PycharmProjects\\Dash game\\assets\\images\\main_player\\player_cube.png")  # пока что используется Absolute Path. Нужно поменять
    return player_image


def load_background_image():
    background_image = pygame.image.load(
        "C:\\Users\\Ususl\\PycharmProjects\\Dash game\\assets\\images\\background.png")  # пока что используется Absolute Path. Нужно поменять
    return background_image


player_image = load_player_image()
background_image = load_background_image()
