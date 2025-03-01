from models.GameObject import GameObject
from src.constants import *


class SpeedPortal(GameObject):
    """ A class for working with portals that change speed   """

    def __init__(self, type_of_portal, x, y, portal_group, obstacle_speed):
        self.speed = type_of_portal
        image_path = f'{PROJECT_PATH}\\assets\\images\\portals\\{self.speed}x_portal.png'
        super().__init__(image_path, x, y, portal_group)
        self.is_drawn = False
        self.obstacle_speed = obstacle_speed

    def get_obstacle_speed(self):
        return {
            -1: 3,
            1: 6,
            2: 9,
            3: 12,
            4: 15
        }.get(self.speed, 3)

    def update(self):
        if not self.is_drawn:
            self.rect.x -= self.obstacle_speed
        if self.rect.x < -self.rect.width:
            self.is_drawn = True

    def change_obstacle_speed(self, value):
        self.obstacle_speed = value
