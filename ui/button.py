# ui/button.py
import pygame
from utils.constants import NARANJA, NEGRO

class Button:
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = NARANJA
        self.text_color = NEGRO

    def draw(self, surface):
        """Dibuja el botón en la superficie"""
        pygame.draw.rect(surface, self.color, self.rect, border_radius=10)
        texto_surface = self.font.render(self.text, True, self.text_color)
        surface.blit(texto_surface, (self.rect.centerx - texto_surface.get_width()//2,
                                   self.rect.centery - texto_surface.get_height()//2))

    def is_clicked(self, pos):
        """Verifica si el botón fue clickeado"""
        return self.rect.collidepoint(pos)