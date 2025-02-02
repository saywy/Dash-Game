import pygame
import os
import sys
from class_Cube import Cube
from class_Ship import Ship
from class_Wave import Wave
from class_Player import Player
from class_SpeedPortal import SpeedPortal
from class_Surface import Surface
from constants import (WIDTH, HEIGHT, PROJECT_PATH, BLACK, WHITE, load_image, OBSTACLE_SPEED, TRACE_COLOR)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GashGame")
surface_group = pygame.sprite.Group()
object_group = pygame.sprite.Group()
speed_portal_group = pygame.sprite.Group()
circles = [] # След волны рисуется отдельно



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

    # surface_group = pygame.sprite.Group()
    line_height = 50
    sixth_line_y = 595
    for surface in surface_group:
        surface_group.remove(surface)
    for portal in speed_portal_group:
        speed_portal_group.remove(portal)

    with open(filename, 'r') as file:
        lines = file.readlines()
        for y, line in enumerate(lines[:6]):
            for x, char in enumerate(line.strip()):
                if char == '-':
                    surface_y = sixth_line_y if y == 5 else sixth_line_y - (5 - y) * line_height
                    Surface(x * line_height, surface_y, surface_group, OBSTACLE_SPEED)
                elif char == '0':
                    surface_y = sixth_line_y - line_height if y == 5 else sixth_line_y - (5 - y) * line_height * 4
                    SpeedPortal(-1, x * line_height, surface_y, speed_portal_group, OBSTACLE_SPEED)
                elif char == '1':
                    surface_y = sixth_line_y - line_height if y == 5 else sixth_line_y - (5 - y) * line_height * 2
                    SpeedPortal(1, x * line_height, surface_y, speed_portal_group, OBSTACLE_SPEED)
                elif char == '2':
                    surface_y = sixth_line_y - line_height if y == 5 else sixth_line_y - (5 - y) * line_height * 1.5
                    SpeedPortal(2, x * line_height, surface_y, speed_portal_group, OBSTACLE_SPEED)
                elif char == '3':
                    surface_y = sixth_line_y - line_height if y == 5 else sixth_line_y - (5 - y) * line_height * 1.75
                    SpeedPortal(3, x * line_height, surface_y, speed_portal_group, OBSTACLE_SPEED)
                elif char == '4':
                    surface_y = sixth_line_y - line_height if y == 5 else sixth_line_y - (5 - y) * line_height * 2
                    SpeedPortal(4, x * line_height, surface_y, speed_portal_group, OBSTACLE_SPEED)


def main_menu_loop(menu, game_object, clock):
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
        game_object.reset_position()
        menu.draw()
        clock.tick(60)


def main():
    """ Основная функция игры   """

    clock = pygame.time.Clock()
    menu = MainMenu()
    game_object = Player(Ship, surface_group, object_group, f"{PROJECT_PATH}\\assets\\images\\main_player\\player_cube.png", 100, HEIGHT - 100, OBSTACLE_SPEED)
    running = True
    in_game = False
    obstacle_speed = OBSTACLE_SPEED

    while running:
        if in_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and isinstance(game_object.mode, Cube):
                    game_object.mode.jump()
            screen.fill(WHITE)
            for surface in surface_group:
                surface.update()
                surface.draw(screen)
            for portal in speed_portal_group:
                portal.update()
                portal.draw(screen)
            if speed := game_object.colide_with_speed_portal(speed_portal_group):
                for surface in surface_group:
                    surface.change_obstacle_speed(speed)
                for portal in speed_portal_group:
                    portal.change_obstacle_speed(speed)
                obstacle_speed = speed
                game_object.mode.obstacle_speed = speed

            for circle in circles:
                circle[2][0] -= obstacle_speed
                pygame.draw.circle(circle[0], circle[1], circle[2], circle[3])
            game_object.update()
            object_group.draw(screen)

            # След волны
            if isinstance(game_object.mode, Wave):
                rect = game_object.mode.rect
                x = rect.x
                y = rect.y
                right = rect.right
                bottom = rect.bottom
                center = [x + (right - x) / 2, y + (bottom - y) / 2]
                circles.append([screen, TRACE_COLOR, center, 10])

            if all(surface.is_drawn for surface in game_object.surface_group):
                in_game = False

            if isinstance(game_object.mode, Cube) and game_object.mode.is_falling() == 'BAD':
                game_object.mode.reset_position()
                in_game = False
            elif isinstance(game_object.mode, Wave) and game_object.mode.in_game is False:
                in_game = False
        else:
            if main_menu_loop(menu, game_object.mode, clock):
                in_game = True
                load_level(f"{PROJECT_PATH}\\assets\\levels\\lvl1.txt")
                game_object.surface_group = surface_group
                game_object.mode.reset_position()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
