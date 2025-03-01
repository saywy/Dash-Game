import os

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
TRACE_COLOR = (53, 68, 61)
PROJECT_PATH = os.path.dirname(__file__)[:-3]

SKIN_CUBE = f"{PROJECT_PATH}\\assets\\images\\main_player\\player_cube.png"
SKIN_SHIP = f"{PROJECT_PATH}\\assets\\images\\main_player\\player_ship.png"
SKIN_WAVE_STRAIGHT = f"{PROJECT_PATH}\\assets\\images\\main_player\\wave\\wave_straight.png"
