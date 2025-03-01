import pygame
import os
import sys

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

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GashGame")
surface_group = pygame.sprite.Group()
object_group = pygame.sprite.Group()
speed_portal_group = pygame.sprite.Group()
circles = []  # След волны рисуется отдельно

class GameObject(pygame.sprite.Sprite):
    """ Родительский класс для всех видов игры """

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
    """ Главное меню игры. """

    def __init__(self):
        self.background = load_image(rf'{PROJECT_PATH}\assets\images\menu_background.webp')
        self.lvl1_button = load_image(rf'{PROJECT_PATH}\assets\images\lvl1.png')
        self.lvl2_button = load_image(rf'{PROJECT_PATH}\assets\images\lvl2.png')
        self.lvl3_button = load_image(rf'{PROJECT_PATH}\assets\images\lvl3.png')
        self.buttons = [self.lvl1_button, self.lvl2_button, self.lvl3_button]
        self.button_rects = []
        self.selected_level = 1

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
                    return True  # Return True to signal level selection
        return False


def load_level(filename):
    """ Подгрузка уровня с текстового файла. """

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
                return menu.selected_level # Return selected level
        clock.tick(60)

class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, surface_group, object_group, obstacle_speed, skin_path):
        super().__init__(object_group)
        self.image = pygame.image.load(skin_path)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.initial_x = x
        self.initial_y = y
        self.speed_up = 3
        self.speed_down = FALL_STRENGTH
        self.is_moving_up = False
        self.current_angle = 0
        self.target_angle = 0
        self.velocity_y = 0
        self.original_image = self.image
        self.surface_group = surface_group
        self.obstacle_speed = obstacle_speed

    def game_over(self):
        global in_game
        in_game = False
        self.reset_position()  # Сбрасываем позицию корабля (если это нужно)

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

        # Проверка столкновения с платформами
        for surface in self.surface_group:
            if self.rect.colliderect(surface.rect):
                self.game_over()  # Переход в главное меню
                break  # Выход из цикла после первого столкновения

        self.rect.y += self.velocity_y
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

        self.current_angle = self.target_angle
        self.image = pygame.transform.rotate(self.original_image, self.current_angle)
        self.rect = self.image.get_rect(center=self.rect.center)

class SpeedPortal(GameObject):
    def __init__(self, type_of_portal, x, y, portal_group, obstacle_spped):
        self.speed = type_of_portal
        image_path = f'{PROJECT_PATH}\\assets\\images\\portals\\{self.speed}x_portal.png'
        super().__init__(image_path, x, y, portal_group)
        self.rect.x = x
        self.rect.y = y
        self.is_drawn = False
        self.obstacle_speed = obstacle_spped
        if self.speed == -1:
            self.image = f'{PROJECT_PATH}\\assets\\images\\portals\\-1x_portal.png'
        elif self.speed == 1:
            self.image = f'{PROJECT_PATH}\\assets\\images\\portals\\1x_portal.png'
        elif self.speed == 2:
            self.image = f'{PROJECT_PATH}\\assets\\images\\portals\\2x_portal.png'
        elif self.speed == 3:
            self.image = f'{PROJECT_PATH}\\assets\\images\\portals\\3x_portal.png'
        elif self.speed == 4:
            self.image = f'{PROJECT_PATH}\\assets\\images\\portals\\4x_portal.png'
        super().__init__(self.image, x, y, portal_group)
        self.rect.x = x
        self.rect.y = y
        self.is_drawn = False
        self.obstacle_speed = obstacle_spped

    def get_obstacle_speed(self):
        if self.speed == -1:
            obstacle_speed = 3
        elif self.speed == 1:
            obstacle_speed = 6
        elif self.speed == 2:
            obstacle_speed = 9
        elif self.speed == 3:
            obstacle_speed = 12
        else:
            obstacle_speed = 15
        return obstacle_speed

    def update(self):
        if not self.is_drawn:
            self.rect.x -= self.obstacle_speed
        if self.rect.x < -self.rect.width:
            self.is_drawn = True

    def change_obstacle_speed(self, value):
        self.obstacle_speed = value


SKIN_CUBE = f"{PROJECT_PATH}\\assets\\images\\main_player\\player_cube.png"
SKIN_SHIP = f"{PROJECT_PATH}\\assets\\images\\main_player\\player_ship.png"
SKIN_WAVE_STRAIGHT = f"{PROJECT_PATH}\\assets\\images\\main_player\\wave\\wave_straight.png"


class Player:
    def __init__(self, mode_class, x, y, surface_group, object_group, skin, obstacle_speed):
        self.mode = mode_class(x, y, surface_group, object_group, skin, obstacle_speed)
        self.surface_group = surface_group
        self.object_group = object_group

    def change_mode(self, mode_class, skin):
        self.mode = mode_class(self.mode.rect.x, self.mode.rect.y, self.surface_group, self.object_group, skin, self.mode.obstacle_speed)


    def update(self):
        self.mode.update()

    def colide_with_speed_portal(self, portal_group):
        for portal in portal_group:
            if self.mode.rect.colliderect(portal.rect):
                if isinstance(portal, SpeedPortal):
                    return portal.get_obstacle_speed()
        return False


class Cube(pygame.sprite.Sprite):
#  TODO: Возможен двойной прыжок

    def __init__(self, x, y, surface_group, object_group, skin, obstacle_speed):
        pygame.sprite.Sprite.__init__(self, object_group) # Инициализация как Sprite
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


SKIN = f"{PROJECT_PATH}\\assets\\images\\main_player\\player_cube.png"


class Surface(GameObject):

#  TODO: Отображение нижней платформы

    def __init__(self, x, y, surface_group, obstacle_speed):
        super().__init__(f'{PROJECT_PATH}\\assets\\images\\cub.png', x, y, surface_group)
        self.is_drawn = False
        self.obstacle_speed = obstacle_speed

    @staticmethod
    def is_dangerous():
        return False

    def change_obstacle_speed(self, value):
        self.obstacle_speed = value

    def update(self):
        if not self.is_drawn:
            self.rect.x -= self.obstacle_speed
        if self.rect.x < -self.rect.width:
            self.is_drawn = True


class Wave(GameObject):
#  TODO: Подправить работу линии - траектории движения

    def __init__(self, x, y, surface_group, object_group, skin, obstacle_speed):
        pygame.sprite.Sprite.__init__(self, object_group)
        self.image = pygame.image.load(skin)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity_y = 0
        self.rect.x = x
        self.is_moving_up = False
        self.surface_group = surface_group
        self.object_group = object_group
        self.height = self.rect.bottom - self.rect.top
        self.skin = skin
        self.in_game = True
        self.obstacle_speed = obstacle_speed

    def update(self):
        keys = pygame.key.get_pressed()
        self.is_moving_up = keys[pygame.K_SPACE]
        for surface in self.surface_group:
            if self.rect.colliderect(surface.rect):
                self.in_game = False

        if self.is_moving_up:
            self.velocity_y = -self.obstacle_speed if self.rect.top > 0 else 0
        else:
            self.velocity_y = self.obstacle_speed if self.rect.bottom < HEIGHT else 0

        if self.is_moving_up and not self.rect.bottom - self.height <= 0:
            self.image = pygame.image.load(
                f"{PROJECT_PATH}\\assets\\images\\main_player\\wave\\wave_up.png")  # наклон вверх
        else:
            if self.rect.bottom >= HEIGHT or self.rect.bottom - self.height <= 0:
                self.image = pygame.image.load(
                    f"{PROJECT_PATH}\\assets\\images\\main_player\\wave\\wave_straight.png")  # без наклона
            else:
                self.image = pygame.image.load(
                    f"{PROJECT_PATH}\\assets\\images\\main_player\\wave\\wave_down.png")  # наклон вниз

        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.y += self.velocity_y

    def reset_position(self):
        self.rect.x = 200
        self.in_game = True
        self.velocity_y = 0
        self.is_moving_up = False

def main():
    """ Основная функция игры """

    clock = pygame.time.Clock()
    menu = MainMenu()
    running = True
    in_game = False
    obstacle_speed = OBSTACLE_SPEED
    game_object = None
    circles = []

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

            game_object.update()
            object_group.draw(screen)

            # След волны
            if isinstance(game_object.mode, Wave):
                rect = game_object.mode.rect
                center = [(rect.left + rect.right) // 2, (rect.top + rect.bottom) // 2]
                circles.append([screen, TRACE_COLOR, center, 10])

            # Условие завершения игры
            if all(surface.is_drawn for surface in surface_group) or \
                    (isinstance(game_object.mode, Cube) and game_object.mode.is_falling() == 'BAD') or \
                    (isinstance(game_object.mode, Wave) and not game_object.mode.in_game):
                in_game = False
                circles = []

        else:
            # Переход в главное меню
            selected_level = main_menu_loop(menu, game_object, clock)
            if selected_level:
                in_game = True
                level_file = f"{PROJECT_PATH}\\assets\\levels\\lvl{selected_level}.txt"
                load_level(level_file)
                object_group.empty()
                skin = f'{PROJECT_PATH}\\assets\\images\\main_player\\player_ship.png'
                x, y = 100, HEIGHT - 100

                # Создание объекта игрока в зависимости от выбранного уровня
                if selected_level == 1:
                    game_object = Player(Cube, x, y, surface_group, object_group, SKIN_CUBE, obstacle_speed)
                elif selected_level == 2:
                    game_object = Player(Ship, x, y, surface_group, object_group, SKIN_SHIP, skin)
                elif selected_level == 3:
                    game_object = Player(Wave, x, y, surface_group, object_group, SKIN_WAVE_STRAIGHT, obstacle_speed)

                game_object.mode.reset_position()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()