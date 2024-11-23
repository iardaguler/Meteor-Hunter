import pygame


class Laser(pygame.sprite.Sprite):
    def __init__(self, file_path,x,y,x_velocity,y_velocity):
        super().__init__()
        self.image = pygame.image.load(file_path)
        self.rect = self.image.get_rect(center=(x, y))
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity

    def update(self):
        # Lazerin yukarı doğru hareket etmesi
        self.rect.y -= self.y_velocity   # Lazerin hızını ayarlayabilirsiniz
        self.rect.x += self.x_velocity

        # Lazer ekranın dışına çıkarsa sil
        if self.rect.bottom < 0:
            self.kill()
