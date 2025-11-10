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

    def draw(self, surface, tile_map, player, imagenes_navegante, navegante_rio1, peces=None, navegante_especial=None, navegante_pescando=None, obstaculos=None):
        """Dibuja la pantalla del juego"""
        # Dibujar mapa de tiles
        tile_map.render(surface, self.cam_x, self.cam_y)
        
        # Dibujar peces
        if peces:
            for pez in peces:
                pez.draw(surface, self.cam_x, self.cam_y)
        
        # Dibujar jugador (sprite según acción)
        if player.sprite_especial and navegante_especial is not None:
            # Usar navegante_caido cuando hay colisión con tronco
            sprite_a_usar = navegante_especial
        elif player.pescando and navegante_pescando is not None:
            sprite_a_usar = navegante_pescando
        else:
            sprite_a_usar = imagenes_navegante[player.frame]
            
        surface.blit(
            sprite_a_usar,
            (
                player.x - self.cam_x - sprite_a_usar.get_width() // 2,
                player.y - self.cam_y - sprite_a_usar.get_height() // 2,
            ),
        )
        
        # Dibujar obstáculos encima del jugador
        if obstaculos:
            for obstaculo in obstaculos:
                obstaculo.draw(surface, self.cam_x, self.cam_y, tile_map)
        
        self.hud.draw_vida(surface, player.vida)
        self.hud.draw_contador_peces(surface, player.peces_recolectados)
        self.hud.draw_tiempo(surface, player.tiempo_inicio, getattr(player, 'dificultad', 'novato'))
        self.hud.draw_mensaje(surface, player.mensaje_turbulencia, player.tiempo_mensaje, player.x, player.y, self.cam_x, self.cam_y)
        
        # Dibujar mensaje de pez
        if player.tiempo_mensaje_pez > 0:
            self.hud.draw_mensaje_pez(surface, player.mensaje_pez, player.x, player.y, self.cam_x, self.cam_y)
        
        # Dibujar mensaje de tronco
        if player.tiempo_colision_tronco > 0:
            self.hud.draw_mensaje_tronco(surface, player.mensaje_tronco, player.x, player.y, self.cam_x, self.cam_y)
        
        self.boton_volver.draw(surface)
        self.boton_x.draw(surface)
    
    def handle_click(self, pos):
        """Maneja los clicks en la pantalla de juego"""
        if self.boton_volver.is_clicked(pos):
            return "volver"
        elif self.boton_x.is_clicked(pos):
            return "salir"
        return None