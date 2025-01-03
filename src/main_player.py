import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.original_image = image
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(400, 360))
        self.velocity_y = 0
        self.gravity = 0.5
        self.is_jumping = False
        self.rotation_angle = 0
        self.rotation_step = 10
        self.jump_height = 150
        self.ground_level = 360

    def update(self):
        if self.is_jumping:
            self.velocity_y -= self.gravity
            self.rect.y -= self.velocity_y
            self.rotation_angle -= self.rotation_step
            if self.rotation_angle < 0:
                self.rotation_angle += 360
            if self.rect.y >= self.ground_level:
                self.rect.y = self.ground_level
                self.is_jumping = False
                self.velocity_y = 0
                if self.rotation_angle % 180 != 0:
                    if self.rotation_angle % 360 == 90 or self.rotation_angle % 360 == 270:
                        self.rotation_angle = 90
                    else:
                        self.rotation_angle = 0
        if self.rect.y < self.ground_level - self.jump_height:
            self.rect.y = self.ground_level - self.jump_height
        self.image = pygame.transform.rotate(self.original_image, self.rotation_angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = 10
