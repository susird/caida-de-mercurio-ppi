# ui/game_screen.py
import os
import pygame
from core.settings import ANCHO, ALTO, MAP_ANCHO, MAP_ALTO, FONTS_DIR
from ui.button import Button

class GameScreen:
    def __init__(self):
        self.cam_x = 0
        self.cam_y = 0
        self.setup_button()
    
    def setup_button(self):
        """Configura el botón de volver"""
        # Obtener dimensiones reales de la pantalla
        info = pygame.display.Info()
        screen_w, screen_h = info.current_w, info.current_h
        
        # Botón más pequeño
        boton_ancho, boton_alto = 120, 40
        boton_x = 20  # Margen izquierdo
        boton_y = screen_h - boton_alto - 20  # Margen inferior
        
        font_path = os.path.join(FONTS_DIR, "VT323-Regular.ttf")
        fuente_boton = pygame.font.Font(font_path, 24)
        
        self.boton_volver = Button(boton_x, boton_y, boton_ancho, boton_alto, "VOLVER", fuente_boton)

    def update_camera(self, player_x, player_y):
        """Actualiza la posición de la cámara siguiendo al jugador"""
        self.cam_x = player_x - ANCHO // 2
        self.cam_y = player_y - ALTO // 2
        self.cam_x = max(0, min(MAP_ANCHO - ANCHO, self.cam_x))
        self.cam_y = max(0, min(MAP_ALTO - ALTO, self.cam_y))

    def draw(self, surface, mapa, player, imagenes_navegante, navegante_rio1):
        """Dibuja la pantalla del juego"""
        # Dibujar mapa
        surface.blit(mapa, (-self.cam_x, -self.cam_y))
        
        # Dibujar jugador
        surface.blit(
            imagenes_navegante[player.frame],
            (
                player.x - self.cam_x - navegante_rio1.get_width() // 2,
                player.y - self.cam_y - navegante_rio1.get_height() // 2,
            ),
        )
        
        # Dibujar botón de volver
        self.boton_volver.draw(surface)
    
    def handle_click(self, pos):
        """Maneja los clicks en la pantalla de juego"""
        if self.boton_volver.is_clicked(pos):
            return "volver"
        return None