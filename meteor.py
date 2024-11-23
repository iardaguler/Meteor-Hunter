import pygame.sprite


class Meteor(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, x_velocity, y_velocity):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
    def update(self):
        self.rect.x += self.x_velocity
        self.rect.y += self.y_velocity

        if self.rect.bottom > 1280:
            self.kill()
