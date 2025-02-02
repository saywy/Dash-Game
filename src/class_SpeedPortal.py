from constants import (GameObject, PROJECT_PATH)


class SpeedPortal(GameObject):
    def __init__(self, type_of_portal, x, y, portal_group, obstacle_spped):
        self.speed = type_of_portal
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
