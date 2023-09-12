import pygame
from constants import BLACK, GREEN

class Button(pygame.sprite.Sprite):
    def __init__(self, text, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.font = pygame.font.Font(None, 30)
        text_surface = self.font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=(width//2, height//2))
        self.image.fill(GREEN)
        self.image.blit(text_surface, text_rect)

