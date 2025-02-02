from constants import (PROJECT_PATH, GameObject)


class Surface(GameObject):
    """ Платформа. баг - отображение нижней платформы (чуть выше чем нужно), может быть изменено при необходимости  """

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
