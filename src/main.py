import pygame
import os
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geometry Dash Clone")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAVITY = 0.5
JUMP_STRENGTH = 10
ROTATION_SPEED = 5
OBSTACLE_SPEED = 2
FALL_STRENGTH = 3
MAX_UPWARD_ROTATION = 20
MAX_DOWNWARD_ROTATION = -20


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"File '{fullname}' not found")
        sys.exit()
    img = pygame.image.load(fullname)
    if colorkey is not None:
        img.set_colorkey(colorkey)
    return img


class GameObject:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


class Cube(GameObject):
    def __init__(self, x, y, group):
        super().__init__("C:\\Users\\Ususl\\PycharmProjects\\Dash game\\assets\\images\\main_player\\player_cube.png", x, y)
        self.velocity_y = 0
        self.is_jumping = False
        self.rotation_angle = 0
        self.group = group

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = -JUMP_STRENGTH
            self.is_jumping = True
            self.rotation_angle = 0

    def return_to_menu(self):
        pygame.quit()
        return False

    def is_falling(self):
        self.rect.y += self.velocity_y
        for surface in self.group:
            if self.rect.colliderect(surface.rect):
                if surface.is_dangerous():
                    self.kill()
                if self.velocity_y > 0:
                    self.rect.bottom = surface.rect.top
                    self.is_jumping = False
                    self.velocity_y = 0
                    return True
                elif self.rect.bottom < surface.rect.top:
                    return self.return_to_menu()
                if self.rect.right > surface.rect.left and self.rect.left < surface.rect.right:
                    return self.return_to_menu()

        return False

    def update_image(self):
        self.image = pygame.transform.rotate(
            pygame.image.load("C:\\Users\\Ususl\\PycharmProjects\\Dash game\\assets\\images\\main_player\\player_cube.png"),
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
            self.rotation_angle = 0

        collision_happened = self.is_falling()

        if self.is_jumping and not collision_happened:
            if self.rotation_angle < 360:
                self.rotation_angle += ROTATION_SPEED

        self.update_image()


class Surface(GameObject):
    def __init__(self, x, y):
        super().__init__("C:\\Users\\Ususl\\PycharmProjects\\Dash game\\assets\\images\\cub.png", x, y)
        self.is_drawn = False

    @staticmethod
    def is_dangerous():
        return False

    def update(self):
        if not self.is_drawn:
            self.rect.x -= OBSTACLE_SPEED
        if self.rect.x < -self.rect.width:
            self.is_drawn = True


class Wave(GameObject):
    def __init__(self, x, y):
        super().__init__("C:\\Users\\Ususl\\PycharmProjects\\Dash game\\assets\\images\\main_player\\wave\\wave_straight.png", x, y)
        self.velocity_y = 0
        self.is_moving_up = False

    def update(self):
        keys = pygame.key.get_pressed()
        self.is_moving_up = keys[pygame.K_SPACE]

        if self.is_moving_up:
            self.velocity_y = -5 if self.rect.top > 0 else 0
        else:
            self.velocity_y = 5 if self.rect.bottom < HEIGHT else 0

        self.rect.y += self.velocity_y

        if self.is_moving_up:
            self.image = pygame.image.load(
                "C:\\Users\\Ususl\\PycharmProjects\\Dash game\\assets\\images\\main_player\\wave\\wave_up.png")
        else:
            if self.rect.bottom >= HEIGHT:
                self.image = pygame.image.load(
                    "C:\\Users\\Ususl\\PycharmProjects\\Dash game\\assets\\images\\main_player\\wave\\wave_straight.png")
            else:
                self.image = pygame.image.load(
                    "C:\\Users\\Ususl\\PycharmProjects\\Dash game\\assets\\images\\main_player\\wave\\wave_down.png")

        self.rect = self.image.get_rect(center=self.rect.center)


class Ship(GameObject):
    def __init__(self, x, y):
        super().__init__("C:\\Users\\Ususl\\PycharmProjects\\Dash game\\assets\\images\\main_player\\player_ship.png", x, y)
        self.initial_x = x
        self.initial_y = y
        self.speed_up = 3
        self.speed_down = FALL_STRENGTH
        self.is_moving_up = False
        self.current_angle = 0
        self.target_angle = 0
        self.velocity_y = 0
        self.original_image = self.image

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

        self.rect.y += self.velocity_y
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))
        self.current_angle = self.target_angle
        self.image = pygame.transform.rotate(self.original_image, self.current_angle)
        self.rect = self.image.get_rect(center=self.rect.center)


class MainMenu:
    def __init__(self):
        self.play_button = load_image("C:\\Users\\Ususl\\PycharmProjects\\Dash game\\assets\\images\\button_play.png")

    def draw(self):
        screen.fill(BLACK)
        button_rect = self.play_button.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(self.play_button, button_rect)
        pygame.display.flip()


def load_level(filename):
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


def main():
    clock = pygame.time.Clock()
    menu = MainMenu()
    cube = Cube(100, HEIGHT - 100, [])
    running = True
    in_game = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if in_game:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    cube.jump()
            else:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    button_rect = menu.play_button.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                    if button_rect.collidepoint(event.pos):
                        in_game = True
                        cube.group = load_level("C:\\Users\\Ususl\\PycharmProjects\\Dash game\\levels\\lvl1.txt")

        if in_game:
            screen.fill(WHITE)
            for surface in cube.group:
                surface.update()
                surface.draw(screen)

            cube.update()
            cube.draw(screen)

            if all(surface.is_drawn for surface in cube.group):
                in_game = False
        else:
            menu.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()