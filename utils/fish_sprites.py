# utils/fish_sprites.py
import pygame
import math

def create_fish_sprite(color, size=18):
    """Crea un sprite de pez realista y bonito"""
    # Superficie más grande con transparencia
    fish = pygame.Surface((size * 2, int(size * 1.2)), pygame.SRCALPHA)
    
    # Cuerpo principal (elipse más grande)
    body_rect = pygame.Rect(size//3, size//5, size, int(size * 0.6))
    pygame.draw.ellipse(fish, color, body_rect)
    
    # Degradado en el cuerpo
    highlight_color = (min(255, color[0] + 40), min(255, color[1] + 40), min(255, color[2] + 40))
    highlight_rect = pygame.Rect(size//3, size//5, size, size//4)
    pygame.draw.ellipse(fish, highlight_color, highlight_rect)
    
    # Cola más elegante
    tail_points = [
        (0, int(size * 0.6)),
        (size//2, size//3),
        (size//3, int(size * 0.6)),
        (size//2, int(size * 0.9))
    ]
    pygame.draw.polygon(fish, color, tail_points)
    
    # Aleta dorsal más grande
    dorsal_points = [
        (int(size * 0.6), size//5),
        (int(size * 0.9), size//8),
        (int(size * 0.9), int(size * 0.4))
    ]
    pygame.draw.polygon(fish, color, dorsal_points)
    
    # Aleta ventral
    ventral_points = [
        (int(size * 0.7), int(size * 0.8)),
        (int(size * 0.9), int(size * 0.9)),
        (int(size * 0.8), int(size * 1.0))
    ]
    pygame.draw.polygon(fish, color, ventral_points)
    
    # Ojo más grande y detallado
    eye_x = int(size * 1.1)
    eye_y = int(size * 0.5)
    pygame.draw.circle(fish, (255, 255, 255), (eye_x, eye_y), 4)
    pygame.draw.circle(fish, (0, 0, 0), (eye_x, eye_y), 2)
    pygame.draw.circle(fish, (255, 255, 255), (eye_x - 1, eye_y - 1), 1)  # Brillo
    
    # Sombra del cuerpo para profundidad
    shadow_color = (max(0, color[0]-40), max(0, color[1]-40), max(0, color[2]-40))
    shadow_rect = pygame.Rect(size//3, int(size * 0.6), size, size//4)
    pygame.draw.ellipse(fish, shadow_color, shadow_rect)
    
    # Líneas del cuerpo para textura
    line_color = (max(0, color[0]-20), max(0, color[1]-20), max(0, color[2]-20))
    for i in range(3):
        start_x = size//2 + i * size//6
        start_y = int(size * 0.3)
        end_y = int(size * 0.7)
        pygame.draw.line(fish, line_color, (start_x, start_y), (start_x, end_y), 1)
    
    return fish

def get_fish_colors():
    """Retorna colores realistas de peces"""
    return [
        (255, 140, 0),    # Naranja dorado
        (255, 215, 0),    # Dorado
        (50, 205, 50),    # Verde lima
        (255, 69, 0),     # Rojo naranja
        (255, 20, 147),   # Rosa fuerte
        (138, 43, 226),   # Violeta
        (255, 165, 0),    # Naranja
        (34, 139, 34),    # Verde bosque
    ]