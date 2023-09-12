import pygame
import random
from constants import RED, ENEMY_HEIGHT, ENEMY_WIDTH, SCREEN_WIDTH

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([ENEMY_WIDTH, ENEMY_HEIGHT])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
        self.rect.y = -ENEMY_HEIGHT

    def update(self):
        
        self.rect.y += 5