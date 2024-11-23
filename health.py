import pygame
from player import Player

class Health(pygame.sprite.Sprite):
    def __init__(self,file_path,x,y):
        super().__init__()
        self.image = pygame.image.load(file_path)
        self.rect = self.image.get_rect(center=(x,y))
    def update(self):
        pass