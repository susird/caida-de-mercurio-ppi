# ui/hud.py
import os
import pygame
from core.settings import FONTS_DIR
from utils.constants import CREMA, NEGRO

class HUD:
    def __init__(self):
        font_path = os.path.join(FONTS_DIR, "VT323-Regular.ttf")
        self.fuente = pygame.font.Font(font_path, 24)

    def draw_vida(self, surface, vida):
        """Dibuja la barra de vida"""
        # Texto de vida
        vida_texto = f"VIDA: {int(vida)}"
        vida_surface = self.fuente.render(vida_texto, True, CREMA)
        surface.blit(vida_surface, (20, 20))
        
        # Barra de vida visual
        barra_ancho = 200
        barra_alto = 20
        vida_porcentaje = vida / 100
        
        # Fondo de la barra
        pygame.draw.rect(surface, NEGRO, (20, 50, barra_ancho, barra_alto))
        # Vida actual
        color_vida = (255, 0, 0) if vida < 30 else (255, 255, 0) if vida < 60 else (0, 255, 0)
        pygame.draw.rect(surface, color_vida, (20, 50, int(barra_ancho * vida_porcentaje), barra_alto))

    def draw_mensaje(self, surface, mensaje, tiempo_restante):
        """Dibuja mensaje temporal centrado"""
        if tiempo_restante > 0:
            mensaje_surface = self.fuente.render(mensaje, True, (255, 100, 100))
            screen_w = surface.get_width()
            x = screen_w // 2 - mensaje_surface.get_width() // 2
            surface.blit(mensaje_surface, (x, 100))