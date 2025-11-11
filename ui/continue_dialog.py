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
        
        # Calcular posiciones centradas
        dialog_width, dialog_height = 500, 200
        dialog_x = (ANCHO - dialog_width) // 2
        dialog_y = (ALTO - dialog_height) // 2
        
        # Botones centrados dentro del diálogo
        button_width, button_height = 180, 40
        button_y = dialog_y + dialog_height - 60
        
        self.btn_continue = Button(
            dialog_x + 40, button_y,
            button_width, button_height, "CONTINUAR", self.font_text
        )
        
        self.btn_new_game = Button(
            dialog_x + dialog_width - button_width - 40, button_y,
            button_width, button_height, "NUEVO JUEGO", self.font_text
        )
    
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
        # Fondo semi-transparente
        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        # Cuadro de diálogo
        dialog_width, dialog_height = 500, 200
        dialog_x = (ANCHO - dialog_width) // 2
        dialog_y = (ALTO - dialog_height) // 2
        
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
        title_rect = title_text.get_rect(center=(ANCHO // 2, dialog_y + 50))
        surface.blit(title_text, title_rect)
        
        # Mensaje
        message_text = self.font_text.render("¿Quieres continuar donde lo dejaste?", True, (220, 220, 220))
        message_rect = message_text.get_rect(center=(ANCHO // 2, dialog_y + 90))
        surface.blit(message_text, message_rect)
        
        # Botones
        self.btn_continue.draw(surface)
        self.btn_new_game.draw(surface)