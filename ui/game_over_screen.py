# ui/game_over_screen.py
import os
import pygame
from core.settings import ANCHO, ALTO, IMAGES_DIR, FONTS_DIR
from utils.helpers import render_con_borde

class GameOverScreen:
    def __init__(self):
        # Cargar fondo (se escalará dinámicamente en draw)
        fondo_path = os.path.join(IMAGES_DIR, "fondo_game_over.png")
        self.fondo = pygame.image.load(fondo_path)
        
        # Cargar fuentes (misma que el menú principal)
        font_path = os.path.join(FONTS_DIR, "VT323-Regular.ttf")
        self.fuente_titulo = pygame.font.Font(font_path, 72)
        self.fuente_subtitulo = pygame.font.Font(font_path, 36)
    
    def draw(self, surface, reason="death"):
        """Dibuja la pantalla de Game Over"""
        # Reproducir sonido de game over (solo la primera vez)
        if not hasattr(self, 'sound_played'):
            from utils.sound_manager import sound_manager
            sound_manager.play_game_over()
            self.sound_played = True
        
        # Obtener tamaño real de la pantalla
        screen_width, screen_height = surface.get_size()
        
        # Escalar y dibujar fondo
        fondo_escalado = pygame.transform.scale(self.fondo, (screen_width, screen_height))
        surface.blit(fondo_escalado, (0, 0))
        
        # Texto "GAME OVER"
        titulo_texto = render_con_borde("GAME OVER", self.fuente_titulo, (255, 255, 255), (0, 0, 0))
        titulo_x = screen_width // 2 - titulo_texto.get_width() // 2
        titulo_y = screen_height // 2 - 100
        surface.blit(titulo_texto, (titulo_x, titulo_y))
        
        # Mensaje según la razón del game over
        if reason == "timeout":
            mensaje = "No lograste recolectar todos los peces a tiempo"
        else:
            mensaje = "Has muerto por consumir tanto mercurio"
        
        subtitulo_texto = render_con_borde(mensaje, self.fuente_subtitulo, (255, 255, 255), (0, 0, 0))
        subtitulo_x = screen_width // 2 - subtitulo_texto.get_width() // 2
        subtitulo_y = titulo_y + 120
        surface.blit(subtitulo_texto, (subtitulo_x, subtitulo_y))
        
        # Instrucción para continuar
        instruccion_texto = render_con_borde("Presiona ESC para volver al menú", self.fuente_subtitulo, (200, 200, 200), (0, 0, 0))
        instruccion_x = screen_width // 2 - instruccion_texto.get_width() // 2
        instruccion_y = subtitulo_y + 80
        surface.blit(instruccion_texto, (instruccion_x, instruccion_y))
    
    def handle_events(self, events):
        """Maneja eventos de la pantalla de Game Over"""
        for event in events:
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
        return None