# utils/tree_loader.py
import pygame
import os
import random

def load_tree_tiles():
    """Carga todos los tiles de árboles disponibles"""
    tree_tiles = []
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_path = os.path.join(script_dir, "assets", "images") + os.sep
    
    # Cargar todos los tiles de árboles (tree1.png a tree9.png)
    for i in range(1, 10):
        tree_path = base_path + f"tree{i}.png"
        if os.path.exists(tree_path):
            try:
                tree_tile = pygame.image.load(tree_path)
                # Escalar a diferentes tamaños para variedad
                for scale in [0.5, 0.75, 1.0, 1.25, 1.5]:
                    size = int(32 * scale)  # Tamaños desde 16 hasta 48 píxeles
                    scaled_tree = pygame.transform.scale(tree_tile, (size, size))
                    tree_tiles.append(scaled_tree)
            except:
                print(f"Error cargando {tree_path}")
    

    return tree_tiles

def load_bush_tiles():
    """Carga todos los tiles de arbustos disponibles"""
    bush_tiles = []
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_path = os.path.join(script_dir, "assets", "images") + os.sep
    
    # Cargar todos los tiles de arbustos (arbusto.png a arbusto6.png)
    bush_files = ['arbusto.png', 'arbusto2.png', 'arbusto3.png', 'arbusto4.png', 'arbusto5.png', 'arbusto6.png']
    
    for bush_file in bush_files:
        bush_path = base_path + bush_file
        if os.path.exists(bush_path):
            try:
                bush_tile = pygame.image.load(bush_path)
                # Escalar a diferentes tamaños para variedad
                for scale in [0.4, 0.6, 0.8, 1.0, 1.2]:
                    size = int(24 * scale)  # Tamaños desde 10 hasta 29 píxeles
                    scaled_bush = pygame.transform.scale(bush_tile, (size, size))
                    bush_tiles.append(scaled_bush)
            except:
                print(f"Error cargando {bush_path}")
    

    return bush_tiles

def load_flower_tiles():
    """Carga tiles de flores disponibles"""
    flower_tiles = []
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_path = os.path.join(script_dir, "assets", "images") + os.sep
    
    flower_path = base_path + "flor10.png"
    if os.path.exists(flower_path):
        try:
            flower_tile = pygame.image.load(flower_path)
            # Diferentes tamaños para la flor
            for scale in [0.3, 0.5, 0.7, 0.9]:
                size = int(16 * scale)
                scaled_flower = pygame.transform.scale(flower_tile, (size, size))
                flower_tiles.append(scaled_flower)
        except:
            print(f"Error cargando {flower_path}")
    

    return flower_tiles

def load_rock_tiles():
    """Carga todos los tiles de rocas disponibles"""
    rock_tiles = []
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_path = os.path.join(script_dir, "assets", "images") + os.sep
    
    # Cargar todos los tiles de rocas (roca1.png a roca6.png)
    for i in range(1, 7):
        rock_path = base_path + f"roca{i}.png"
        if os.path.exists(rock_path):
            try:
                rock_tile = pygame.image.load(rock_path)
                # Escalar a diferentes tamaños para variedad
                for scale in [0.5, 0.7, 1.0, 1.3, 1.6]:
                    size = int(28 * scale)  # Tamaños desde 14 hasta 45 píxeles
                    scaled_rock = pygame.transform.scale(rock_tile, (size, size))
                    rock_tiles.append(scaled_rock)
            except:
                print(f"Error cargando {rock_path}")
    

    return rock_tiles

class VegetationElement:
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite
        
    def draw(self, surface, cam_x, cam_y):
        screen_x = int(self.x - cam_x)
        screen_y = int(self.y - cam_y)
        
        # Solo dibujar si está en pantalla
        if -50 <= screen_x <= surface.get_width() + 50 and -50 <= screen_y <= surface.get_height() + 50:
            sprite_rect = self.sprite.get_rect(center=(screen_x, screen_y))
            surface.blit(self.sprite, sprite_rect)