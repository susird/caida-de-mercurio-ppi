import os
import pygame
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
SOUNDS_DIR = ASSETS_DIR / "sounds"
FONTS_DIR = BASE_DIR / "fonts"

pygame.init()
display_info = pygame.display.Info()
SCREEN_WIDTH = display_info.current_w
SCREEN_HEIGHT = display_info.current_h
pygame.quit()

MAP_WIDTH = 8000
MAP_HEIGHT = 20000

WATER_BLUE_LIGHT = (30, 144, 255)
WATER_BLUE_DARK = (20, 100, 200)
LAND_GREEN = (34, 139, 34)
JUNGLE_GREENS = [(0, 120, 0), (0, 100, 0), (0, 150, 50)]
TURBULENCE_BLUE = (0, 60, 120)

BOAT_SPRITE_1 = "navegante_rio1.png"
BOAT_SPRITE_2 = "navegante_rio2.png"

FULLSCREEN_MODE = True