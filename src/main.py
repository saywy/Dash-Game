import pygame
import sys
from models.Ship import Ship
from models.SpeedPortal import SpeedPortal
from models.Cube import Cube
from models.Wave import Wave
from models.Player import Player
from models.Surface import Surface
from constants import *

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🍀 Cube Stories")
surface_group = pygame.sprite.Group()
object_group = pygame.sprite.Group()
speed_portal_group = pygame.sprite.Group()
circles = []


class MainMenu:
    """ The class of the main game menu """

    # TODO Add an animated image instead of a static image

    def __init__(self):
        self.background = self.load_image(rf'{PROJECT_PATH}\assets\images\menu_background.webp')
        self.lvl1_button = self.load_image(rf'{PROJECT_PATH}\assets\images\lvl1.png')
        self.lvl2_button = self.load_image(rf'{PROJECT_PATH}\assets\images\lvl2.png')
        self.lvl3_button = self.load_image(rf'{PROJECT_PATH}\assets\images\lvl3.png')
        self.buttons = [self.lvl1_button, self.lvl2_button, self.lvl3_button]
        self.button_rects = []
        self.selected_level = 1

    def load_image(self, name, colorkey=None):
        fullname = os.path.join(name)
        if not os.path.isfile(fullname):
            print(f"File '{fullname}' not found")
            sys.exit()
        img = pygame.image.load(fullname)
        if colorkey:
            img.set_colorkey(colorkey)
        return img

    def draw(self):
        screen.blit(self.background, (0, 0))
        button_y = HEIGHT // 2 - 50
        button_spacing = 100
        for i, button in enumerate(self.buttons):
            x = WIDTH // 2 - button.get_width() // 2
            y = button_y + i * (button.get_height() + button_spacing)
            rect = button.get_rect(topleft=(x, y))
            screen.blit(button, rect)
            self.button_rects.append(rect)
        pygame.display.flip()

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self.button_rects):
                if rect.collidepoint(event.pos):
                    self.selected_level = i + 1
                    return True
        return False


def load_level(filename):
    """ Loads a level from a text file  """
    # TODO Upload paths may not work correctly on some computers.

    surface_group.empty()
    speed_portal_group.empty()
    line_height = 50
    sixth_line_y = 595
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            for y, line in enumerate(lines[:6]):
                for x, char in enumerate(line.strip()):
                    if char == '-':
                        surface_y = sixth_line_y if y == 5 else sixth_line_y - (5 - y) * line_height
                        Surface(x * line_height, surface_y, surface_group, OBSTACLE_SPEED)
                    elif char in '01234':
                        surface_y = sixth_line_y - line_height if y == 5 else sixth_line_y - (5 - y) * line_height * (
                                5 - int(char)) / 5
                        SpeedPortal(int(char), x * line_height, surface_y, speed_portal_group, OBSTACLE_SPEED)
    except FileNotFoundError:
        print(f"Error: Level file '{filename}' not found.")
        sys.exit()


def main_menu_loop(menu, game_object, clock):
    in_menu = True
    while in_menu:
        menu.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if menu.handle_input(event):
                return menu.selected_level
        clock.tick(60)


def main():
    """ Start the game! """

    clock = pygame.time.Clock()
    menu = MainMenu()
    running = True
    in_game = False
    game_object = None

    while running:
        if in_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and isinstance(game_object.mode, Cube):
                    game_object.mode.jump()

            screen.fill(WHITE)
            surface_group.update()
            surface_group.draw(screen)
            speed_portal_group.update()
            speed_portal_group.draw(screen)

            if speed := game_object.colide_with_speed_portal(speed_portal_group):
                for surface in surface_group:
                    surface.change_obstacle_speed(speed)
                for portal in speed_portal_group:
                    portal.change_obstacle_speed(speed)
                game_object.mode.obstacle_speed = speed

            game_object.update()
            object_group.draw(screen)

            if isinstance(game_object.mode, Wave):
                rect = game_object.mode.rect
                center = [(rect.left + rect.right) // 2, (rect.top + rect.bottom) // 2]
                circles.append([screen, TRACE_COLOR, center, 10])

            if all(surface.is_drawn for surface in surface_group) or \
                    (isinstance(game_object.mode, Cube) and game_object.mode.is_falling() == 'BAD') or \
                    (isinstance(game_object.mode, Wave) and not game_object.mode.in_game):
                in_game = False
                circles.clear()
        else:
            selected_level = main_menu_loop(menu, game_object, clock)
            if selected_level:
                in_game = True
                level_file = f"{PROJECT_PATH}\\assets\\levels\\lvl{selected_level}.txt"
                load_level(level_file)
                object_group.empty()
                skin = f'{PROJECT_PATH}\\assets\\images\\main_player\\player_ship.png'
                x, y = 100, HEIGHT - 100

                if selected_level == 1:
                    game_object = Player(Cube, x, y, surface_group, object_group, SKIN_CUBE, OBSTACLE_SPEED)
                elif selected_level == 2:
                    game_object = Player(Ship, x, y, surface_group, object_group, SKIN_SHIP, skin)
                elif selected_level == 3:
                    game_object = Player(Wave, x, y, surface_group, object_group, SKIN_WAVE_STRAIGHT, OBSTACLE_SPEED)

                game_object.mode.reset_position()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
