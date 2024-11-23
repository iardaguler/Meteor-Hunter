import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self,file_path,file_path_left,file_path_right,x,y,velocity):
        super().__init__()
        self.image = pygame.image.load(file_path)
        self.rect = self.image.get_rect(center=(x,y))
        self.file_path_left = file_path_left
        self.file_path_right = file_path_right
        self.file_path = file_path
        self.velocity = velocity
    def update(self):
        keys = pygame.key.get_pressed()
        self.image = pygame.image.load(self.file_path)
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.velocity
            self.image = pygame.image.load(self.file_path_left)
        if keys[pygame.K_d] and self.rect.right < 1280:
            self.rect.x += self.velocity
            self.image = pygame.image.load(self.file_path_right)