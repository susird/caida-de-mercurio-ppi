# ui/main_menu.py
import os
import pygame
from core.settings import ANCHO, ALTO, IMAGES_DIR, FONTS_DIR
from utils.constants import CREMA, NEGRO
from utils.helpers import render_con_borde
from ui.button import Button

class FondoInicio:
    def __init__(self):
        self.size = pygame.Vector2(ANCHO, ALTO)
        self.coord = pygame.Vector2(0, 0)
        self.imagen = None
        self.posicion = 0

    def load(self):
        """Carga la imagen del fondo después de inicializar pygame.display."""
        # Actualizar dimensiones actuales de pantalla
        self.size = pygame.Vector2(ANCHO, ALTO)
        
        archivo = os.path.join(IMAGES_DIR, "fondo_pixelado.png")
        if not os.path.exists(archivo):
            raise FileNotFoundError(f"No se encontró el archivo de fondo: {archivo}")

        # Estirar la imagen para que cubra toda la pantalla
        self.imagen = pygame.transform.scale(
            pygame.image.load(archivo).convert_alpha(),
            (int(self.size.x), int(self.size.y))
        )
        self.coord.x = 0
        self.coord.y = 0

class MainMenu:
    def __init__(self):
        self.fondo = FondoInicio()
        self.setup_fonts()
        self.setup_button()

    def setup_fonts(self):
        """Configura las fuentes del menú"""
        font_path = os.path.join(FONTS_DIR, "VT323-Regular.ttf")
        self.fuente_titulo = pygame.font.Font(font_path, 64)
        self.fuente_subtitulo = pygame.font.Font(font_path, 28)
        self.fuente_boton = pygame.font.Font(font_path, 36)

    def setup_button(self):
        """Configura los botones del menú"""
        # Obtener dimensiones reales de la pantalla
        info = pygame.display.Info()
        screen_w, screen_h = info.current_w, info.current_h
        
        boton_ancho, boton_alto = 200, 60
        boton_x = screen_w // 2 - boton_ancho // 2
        
        # Botón jugar
        boton_y_jugar = screen_h - 250
        self.boton_jugar = Button(boton_x, boton_y_jugar, boton_ancho, boton_alto, "JUGAR", self.fuente_boton)
        
        # Botón salir
        boton_y_salir = screen_h - 170
        self.boton_salir = Button(boton_x, boton_y_salir, boton_ancho, boton_alto, "SALIR", self.fuente_boton)

    def draw(self, surface):
        """Dibuja el menú principal"""
        # Obtener dimensiones reales de la pantalla
        screen_w, screen_h = surface.get_size()
        
        # Cargar imagen de fondo y estirarla a las dimensiones reales
        archivo = os.path.join(IMAGES_DIR, "fondo_pixelado.png")
        fondo_original = pygame.image.load(archivo).convert_alpha()
        fondo_estirado = pygame.transform.scale(fondo_original, (screen_w, screen_h))
        surface.blit(fondo_estirado, (0, 0))

        # Dibujar textos
        texto_titulo = render_con_borde("CAÍDA DE MERCURIO", self.fuente_titulo, CREMA, NEGRO)
        texto_subtitulo = render_con_borde("Aventura en aguas envenenadas", self.fuente_subtitulo, CREMA, NEGRO)

        surface.blit(texto_titulo, (screen_w//2 - texto_titulo.get_width()//2, 80))
        surface.blit(texto_subtitulo, (screen_w//2 - texto_subtitulo.get_width()//2, 160))

        # Dibujar botones
        self.boton_jugar.draw(surface)
        self.boton_salir.draw(surface)

    def handle_click(self, pos):
        """Maneja los clicks en el menú"""
        if self.boton_jugar.is_clicked(pos):
            return "jugar"
        elif self.boton_salir.is_clicked(pos):
            return "salir"
        return None