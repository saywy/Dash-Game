import pygame
import os
import sys
from class_Cube import Cube
from class_Ship import Ship
from class_Wave import Wave
from class_Surface import Surface
from constants import (WIDTH, HEIGHT, PROJECT_PATH, BLACK, WHITE)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GashGame")


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"File '{fullname}' not found")
        sys.exit()
    img = pygame.image.load(fullname)
    if colorkey:
        img.set_colorkey(colorkey)
    return img


class MainMenu:
    """
    Главное меню игры.
    Пока что содержит 1 кнопку "играть". Нужно добавить переключаетли уровней и как вариант, какую то систему наград для игрока
    (например какие-то эксклюзивные скины на куб / корабль / волну)
    """

    def __init__(self):
        self.play_button = load_image(rf'{PROJECT_PATH}\assets\images\button_play.png')

    def draw(self):
        screen.fill(BLACK)
        button_rect = self.play_button.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(self.play_button, button_rect)
        pygame.display.flip()


def load_level(filename):
    """ Подгрузка уровня с текстового файла. Не до конца доработано.  """

    surfaces = []
    line_height = 50
    sixth_line_y = 595

    with open(filename, 'r') as file:
        lines = file.readlines()
        for y, line in enumerate(lines[:6]):
            for x, char in enumerate(line.strip()):
                if char == '-':
                    surface_y = sixth_line_y if y == 5 else sixth_line_y - (5 - y) * line_height
                    surface = Surface(x * line_height, surface_y)
                    surfaces.append(surface)

    return surfaces


def main_menu_loop(menu, cube, clock):
    in_menu = True
    while in_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                button_rect = menu.play_button.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                if button_rect.collidepoint(event.pos):
                    return True
        cube.reset_position()
        cube.group = load_level(f"{PROJECT_PATH}\\assets\\levels\\lvl1.txt")
        menu.draw()
        clock.tick(60)


def main():
    """ Основная функция игры   """

    clock = pygame.time.Clock()
    menu = MainMenu()
    cube = Cube(100, HEIGHT - 100, [])
    running = True
    in_game = False

    while running:
        if in_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    cube.jump()
            screen.fill(WHITE)
            for surface in cube.group:
                surface.update()
                surface.draw(screen)

            cube.update()
            cube.draw(screen)

            if all(surface.is_drawn for surface in cube.group):
                in_game = False

            if cube.is_falling() == 'BAD':
                cube.reset_position()
                in_game = False
        else:
            if main_menu_loop(menu, cube, clock):
                in_game = True
                cube.group = load_level(f"{PROJECT_PATH}\\assets\\levels\\lvl1.txt")

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()