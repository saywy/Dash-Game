from class_SpeedPortal import SpeedPortal


class Player:
    def __init__(self, mode, surface_group, object_group, skin,  x, y):
        self.mode = mode(x, y, surface_group, object_group, skin)

    def change_mode(self, mod, surface_group, object_group, skin,  x, y):
        del self.mode
        self.mode = mod(x, y, surface_group, object_group, skin)

    def update(self):
        self.mode.update()

    def colide_with_speed_portal(self, portal_group):
        for portal in portal_group:
            if self.mode.rect.colliderect(portal.rect):
                if isinstance(portal, SpeedPortal):
                    return portal.get_obstacle_speed()
        return False
