import os
import pygame
from core.settings import ANCHO, ALTO, FONTS_DIR, IMAGES_DIR
from data.game_data import GameData

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
        self.font_title = pygame.font.Font(font_path, 48)
        self.font_text = pygame.font.Font(font_path, 24)
        self.font_score = pygame.font.Font(font_path, 20)
        
        self.game_data = GameData()
    
    def draw(self, surface):
        # Dibujar fondo
        surface.blit(self.fondo, (0, 0))
        
        # Título
        titulo = self.font_title.render("¡GANASTE!", True, (0, 0, 0))
        titulo_rect = titulo.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
        surface.blit(titulo, titulo_rect)
        
        # Subtítulo
        subtitulo = self.font_text.render("Lograste pescar 20 peces a tiempo", True, (0, 0, 0))
        subtitulo_rect = subtitulo.get_rect(center=(ANCHO // 2, ALTO // 2 + 50))
        surface.blit(subtitulo, subtitulo_rect)
        
        # Instrucción
        instruccion = self.font_text.render("Presiona ESC para volver al menú", True, (50, 50, 50))
        instruccion_rect = instruccion.get_rect(center=(ANCHO // 2, ALTO // 2 + 150))
        surface.blit(instruccion, instruccion_rect)