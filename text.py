import pygame
from constants import BLACK, FONT_SIZE

class Text(pygame.sprite.Sprite):
    def __init__(self, text, x, y):
        super().__init__()
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.image = self.font.render(text, True, BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y