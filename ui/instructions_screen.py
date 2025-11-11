# ui/instructions_screen.py
import os
import pygame
from core.settings import ANCHO, ALTO, IMAGES_DIR, FONTS_DIR
from utils.constants import CREMA, NEGRO
from utils.helpers import render_con_borde
from ui.button import Button

class InstructionsScreen:
    def __init__(self):
        self.setup_fonts()
        self.setup_buttons()
    
    def setup_fonts(self):
        font_path = os.path.join(FONTS_DIR, "VT323-Regular.ttf")
        self.fuente_titulo = pygame.font.Font(font_path, 48)
        self.fuente_texto = pygame.font.Font(font_path, 24)
        self.fuente_boton = pygame.font.Font(font_path, 32)
    
    def setup_buttons(self):
        info = pygame.display.Info()
        screen_w, screen_h = info.current_w, info.current_h
        
        # Botón Empezar
        boton_ancho, boton_alto = 250, 60
        boton_x = screen_w // 2 - boton_ancho // 2
        boton_y = screen_h - 130
        self.boton_empezar = Button(boton_x, boton_y, boton_ancho, boton_alto, "EMPEZAR A JUGAR", self.fuente_boton)
    
    def draw(self, surface):
        screen_w, screen_h = surface.get_size()
        
        # Fondo oscurecido
        archivo = os.path.join(IMAGES_DIR, "fondo_pixelado.png")
        fondo_original = pygame.image.load(archivo).convert_alpha()
        fondo_estirado = pygame.transform.scale(fondo_original, (screen_w, screen_h))
        surface.blit(fondo_estirado, (0, 0))
        
        # Capa oscura para mejorar legibilidad
        overlay = pygame.Surface((screen_w, screen_h))
        overlay.set_alpha(120)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        # Título
        titulo = render_con_borde("CÓMO JUGAR", self.fuente_titulo, CREMA, NEGRO)
        surface.blit(titulo, (screen_w//2 - titulo.get_width()//2, 50))
        
        # Instrucciones
        instrucciones = [
            "OBJETIVO:",
            "• Recolecta 20 peces antes de que se acabe el tiempo",
            "",
            "CONTROLES:",
            "• Flechas (↑↓←→): Mover el barco",
            "• ESPACIO: Acelerar (turbo)",
            "• S: Pescar (cuando hay peces cerca)",
            "• ESC: Volver al menú / Guardar partida",
            "",
            "TIPOS DE PECES:",
            "• Peces Buenos: Dan +2 vida, valen 2 peces",
            "• Peces Tóxicos: Quitan 4-8 vida, valen 1 pez",
            "",
            "PELIGROS:",
            "• Troncos y Barriles: Quitan vida al chocar",
            "• Turbulencias: Agua contaminada que reduce velocidad",
            "",
            "CONSEJOS:",
            "• Busca peces buenos en zonas de turbulencia",
            "• Usa el turbo para escapar del peligro",
            "• Evita obstáculos para conservar vida"
        ]
        
        y_pos = 120
        for linea in instrucciones:
            if linea.startswith("•"):
                texto = render_con_borde(linea, self.fuente_texto, CREMA, NEGRO)
                surface.blit(texto, (screen_w//2 - 200, y_pos))
            elif linea.endswith(":"):
                texto = render_con_borde(linea, self.fuente_texto, (255, 255, 100), NEGRO)
                surface.blit(texto, (screen_w//2 - 250, y_pos))
            elif linea == "":
                pass
            else:
                texto = render_con_borde(linea, self.fuente_texto, CREMA, NEGRO)
                surface.blit(texto, (screen_w//2 - texto.get_width()//2, y_pos))
            
            y_pos += 30
        
        # Botón
        self.boton_empezar.draw(surface)
    
    def handle_click(self, pos):
        if self.boton_empezar.is_clicked(pos):
            return "start_game"
        return None