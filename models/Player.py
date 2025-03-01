from models.SpeedPortal import SpeedPortal


class Player:
    """ The glass of working with the main player   """

    def __init__(self, mode_class, x, y, surface_group, object_group, skin, obstacle_speed):
        self.mode = mode_class(x, y, surface_group, object_group, skin, obstacle_speed)
        self.surface_group = surface_group
        self.object_group = object_group

    def change_mode(self, mode_class, skin):
        self.mode = mode_class(self.mode.rect.x, self.mode.rect.y, self.surface_group, self.object_group, skin,
                               self.mode.obstacle_speed)

    def update(self):
        self.mode.update()

    def colide_with_speed_portal(self, portal_group):
        for portal in portal_group:
            if self.mode.rect.colliderect(portal.rect):
                if isinstance(portal, SpeedPortal):
                    return portal.get_obstacle_speed()
        return False
