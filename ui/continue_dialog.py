import pygame
import os
from core.settings import ANCHO, ALTO, FONTS_DIR, IMAGES_DIR
from utils.constants import CREMA, NEGRO
from ui.button import Button

class ContinueDialog:
    def __init__(self):
        font_path = os.path.join(FONTS_DIR, "VT323-Regular.ttf")
        self.font_title = pygame.font.Font(font_path, 32)
        self.font_text = pygame.font.Font(font_path, 24)
        
        # Cargar fondo del diálogo
        self._load_dialog_background()
        
        # Los botones se posicionarán dinámicamente en draw()
        self.dialog_width = 500
        self.dialog_height = 200
        self.button_width = 180
        self.button_height = 40
    
    def _load_dialog_background(self):
        """Carga una porción del fondo del juego para el diálogo"""
        try:
            fondo_path = os.path.join(IMAGES_DIR, "fondo_pixelado.png")
            if os.path.exists(fondo_path):
                full_bg = pygame.image.load(fondo_path)
                # Tomar una sección del fondo y oscurecerla
                section = pygame.Surface((500, 200))
                section.blit(full_bg, (0, 0), (100, 100, 500, 200))
                
                # Oscurecer la sección
                dark_overlay = pygame.Surface((500, 200))
                dark_overlay.set_alpha(120)
                dark_overlay.fill((0, 0, 0))
                section.blit(dark_overlay, (0, 0))
                
                self.dialog_bg = section
            else:
                self.dialog_bg = None
        except:
            self.dialog_bg = None
    
    def handle_click(self, pos):
        if self.btn_continue.is_clicked(pos):
            return "continue"
        elif self.btn_new_game.is_clicked(pos):
            return "new_game"
        return None
    
    def draw(self, surface):
        # Obtener tamaño real de la pantalla
        screen_width, screen_height = surface.get_size()
        
        # Fondo semi-transparente
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        # Cuadro de diálogo
        dialog_width, dialog_height = 500, 200
        dialog_x = (screen_width - dialog_width) // 2
        dialog_y = (screen_height - dialog_height) // 2
        
        # Dibujar fondo del diálogo
        if self.dialog_bg:
            surface.blit(self.dialog_bg, (dialog_x, dialog_y))
        else:
            # Fondo de respaldo con gradiente
            pygame.draw.rect(surface, (40, 60, 80), (dialog_x, dialog_y, dialog_width, dialog_height))
        
        # Borde del diálogo
        pygame.draw.rect(surface, (200, 200, 200), (dialog_x, dialog_y, dialog_width, dialog_height), 3)
        
        # Título
        title_text = self.font_title.render("PARTIDA GUARDADA", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen_width // 2, dialog_y + 50))
        surface.blit(title_text, title_rect)
        
        # Mensaje
        message_text = self.font_text.render("¿Quieres continuar donde lo dejaste?", True, (220, 220, 220))
        message_rect = message_text.get_rect(center=(screen_width // 2, dialog_y + 90))
        surface.blit(message_text, message_rect)
        
        # Crear botones dinámicamente según tamaño de pantalla
        button_y = dialog_y + self.dialog_height - 60
        
        self.btn_continue = Button(
            dialog_x + 40, button_y,
            self.button_width, self.button_height, "CONTINUAR", self.font_text
        )
        
        self.btn_new_game = Button(
            dialog_x + self.dialog_width - self.button_width - 40, button_y,
            self.button_width, self.button_height, "NUEVO JUEGO", self.font_text
        )
        
        # Botones
        self.btn_continue.draw(surface)
        self.btn_new_game.draw(surface)