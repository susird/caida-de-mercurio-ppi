import pygame
from pathlib import Path
from config.settings import IMAGES_DIR
from utils.constants import ANCHO_NAVEGANTE, ALTO_NAVEGANTE

def render_text_with_border(text, font, text_color, border_color):
    text_surface = font.render(text, True, text_color)
    border_surface = font.render(text, True, border_color)
    
    width = text_surface.get_width() + 4
    height = text_surface.get_height() + 4
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    border_offsets = [(-2,0), (2,0), (0,-2), (0,2), (-2,-2), (2,-2), (-2,2), (2,2)]
    for dx, dy in border_offsets:
        surface.blit(border_surface, (dx+2, dy+2))
    
    surface.blit(text_surface, (2, 2))
    return surface

def load_navegantes():
    try:
        sprites = _load_boat_sprites()
        return sprites["frames"], sprites["main"], sprites["special"], sprites["fishing"]
    except Exception as e:
        raise RuntimeError(f"Error cargando sprites del navegante: {e}")

def _load_boat_sprites():
    sprite_files = {
        "main": "navegante_rio1.png",
        "secondary": "navegante_rio2.png", 
        "special": "navegante_caido.png",
        "fishing": "navegante_rio3.png"
    }
    
    sprites = {}
    
    for sprite_type, filename in sprite_files.items():
        sprite_path = Path(IMAGES_DIR) / filename
        
        if sprite_type in ["main", "secondary"] and not sprite_path.exists():
            raise FileNotFoundError(f"Sprite requerido no encontrado: {sprite_path}")
        
        if sprite_path.exists():
            try:
                image = pygame.image.load(str(sprite_path)).convert_alpha()
                sprites[sprite_type] = pygame.transform.scale(image, (ANCHO_NAVEGANTE, ALTO_NAVEGANTE))
            except pygame.error as e:
                raise RuntimeError(f"Error cargando {filename}: {e}")
        else:
            sprites[sprite_type] = None
    
    return {
        "frames": [sprites["main"], sprites["secondary"]],
        "main": sprites["main"],
        "special": sprites["special"],
        "fishing": sprites["fishing"]
    }

# Mantener compatibilidad
render_con_borde = render_text_with_border