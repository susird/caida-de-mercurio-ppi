# core/settings.py
import os
import pygame

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")
FONTS_DIR = os.path.join(BASE_DIR, "fonts")

# Obtener dimensiones de la pantalla
pygame.init()
info = pygame.display.Info()
ANCHO = info.current_w
ALTO = info.current_h
pygame.quit()
MAP_ANCHO = 8000
MAP_ALTO = 20000  # Mapa mucho más largo

# Colores
AZUL1 = (30, 144, 255)   # azul claro
AZUL2 = (20, 100, 200)   # azul oscuro
VERDE = (34, 139, 34)
SELVAS = [(0, 120, 0), (0, 100, 0), (0, 150, 50)]
TURBULENCIA = (0, 60, 120)

# Nombres de archivos en assets/images/
NAVEGANTE_1 = "navegante_rio1.png"
NAVEGANTE_2 = "navegante_rio2.png"
VECTOR = pygame.math.Vector2
FULLSCREEN = True