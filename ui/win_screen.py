# ui/win_screen.py
import os
import pygame
from core.settings import ANCHO, ALTO, FONTS_DIR, IMAGES_DIR

class WinScreen:
    def __init__(self):
        # Cargar fondo de victoria
        fondo_path = os.path.join(IMAGES_DIR, "win_fondo.png")
        if os.path.exists(fondo_path):
            self.fondo = pygame.image.load(fondo_path)
            self.fondo = pygame.transform.scale(self.fondo, (ANCHO, ALTO))
        else:
            # Fondo de respaldo
            self.fondo = pygame.Surface((ANCHO, ALTO))
            self.fondo.fill((0, 150, 0))  # Verde
        
        # Cargar fuente
        font_path = os.path.join(FONTS_DIR, "VT323-Regular.ttf")
        self.fuente_titulo = pygame.font.Font(font_path, 72)
        self.fuente_texto = pygame.font.Font(font_path, 36)
    
    def draw(self, surface):
        # Dibujar fondo
        surface.blit(self.fondo, (0, 0))
        
        # Texto principal
        titulo = self.fuente_titulo.render("GANASTE", True, (255, 255, 255))
        titulo_rect = titulo.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
        surface.blit(titulo, titulo_rect)
        
        # Subtítulo
        subtitulo = self.fuente_texto.render("Lograste pescar 20 peces a tiempo", True, (255, 255, 255))
        subtitulo_rect = subtitulo.get_rect(center=(ANCHO // 2, ALTO // 2 + 50))
        surface.blit(subtitulo, subtitulo_rect)
        
        # Instrucción
        instruccion = self.fuente_texto.render("Presiona ESC para volver al menú", True, (200, 200, 200))
        instruccion_rect = instruccion.get_rect(center=(ANCHO // 2, ALTO // 2 + 150))
        surface.blit(instruccion, instruccion_rect)