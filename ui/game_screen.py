# ui/game_screen.py
import os
import pygame
from core.settings import ANCHO, ALTO, MAP_ANCHO, MAP_ALTO, FONTS_DIR
from ui.button import Button
from ui.hud import HUD

class GameScreen:
    def __init__(self):
        self.cam_x = 0
        self.cam_y = 0
        self.hud = HUD()
        self.setup_button()
    
    def setup_button(self):
        info = pygame.display.Info()
        screen_w, screen_h = info.current_w, info.current_h
        
        font_path = os.path.join(FONTS_DIR, "VT323-Regular.ttf")
        fuente_boton = pygame.font.Font(font_path, 24)
        
        boton_ancho, boton_alto = 120, 40
        boton_x = 20
        boton_y = screen_h - boton_alto - 20
        self.boton_volver = Button(boton_x, boton_y, boton_ancho, boton_alto, "VOLVER", fuente_boton)
        
        x_size = 50
        x_x = screen_w - x_size - 20
        x_y = 20
        fuente_x = pygame.font.Font(font_path, 36)
        self.boton_x = Button(x_x, x_y, x_size, x_size, "X", fuente_x)

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
        
        self.hud.draw_vida(surface, player.vida)
        self.hud.draw_mensaje(surface, player.mensaje_turbulencia, player.tiempo_mensaje)
        
        self.boton_volver.draw(surface)
        self.boton_x.draw(surface)
    
    def handle_click(self, pos):
        """Maneja los clicks en la pantalla de juego"""
        if self.boton_volver.is_clicked(pos):
            return "volver"
        elif self.boton_x.is_clicked(pos):
            return "salir"
        return None