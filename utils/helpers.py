# utils/helpers.py
import os
import pygame
from core.settings import IMAGES_DIR
from utils.constants import ANCHO_NAVEGANTE, ALTO_NAVEGANTE

def render_con_borde(texto, fuente, color_texto, color_borde):
    """Función para renderizar texto con borde"""
    texto_surface = fuente.render(texto, True, color_texto)
    borde_surface = fuente.render(texto, True, color_borde)
    superficie = pygame.Surface((texto_surface.get_width() + 4, texto_surface.get_height() + 4), pygame.SRCALPHA)
    for dx, dy in [(-2,0),(2,0),(0,-2),(0,2), (-2,-2),(2,-2),(-2,2),(2,2)]:
        superficie.blit(borde_surface, (dx+2, dy+2))
    superficie.blit(texto_surface, (2, 2))
    return superficie

def load_navegantes():
    """Carga las imágenes del navegante y devuelve (lista_de_frames, primer_frame)."""
    ruta1 = os.path.join(IMAGES_DIR, "navegante_rio1.png")
    ruta2 = os.path.join(IMAGES_DIR, "navegante_rio2.png")

    if not os.path.exists(ruta1) or not os.path.exists(ruta2):
        raise FileNotFoundError("No se encontraron las imágenes de navegantes en /assets/images/")

    img1 = pygame.image.load(ruta1).convert_alpha()
    img2 = pygame.image.load(ruta2).convert_alpha()

    # Escalar las imágenes al tamaño deseado
    img1 = pygame.transform.scale(img1, (ANCHO_NAVEGANTE, ALTO_NAVEGANTE))
    img2 = pygame.transform.scale(img2, (ANCHO_NAVEGANTE, ALTO_NAVEGANTE))

    return [img1, img2], img1