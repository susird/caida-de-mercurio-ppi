# utils/tile_generator.py
import pygame
import random
import os
from core.settings import AZUL1, AZUL2, VERDE, SELVAS

TILE_SIZE = 32

def create_water_tile(variant=0):
    """Crea tiles de agua con diferentes patrones"""
    tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
    
    if variant == 0:  # Agua clara
        tile.fill(AZUL1)
        # Solo variaciones muy sutiles
        for i in range(2):
            x = random.randint(0, TILE_SIZE)
            y = random.randint(0, TILE_SIZE)
            color_var = (max(0, min(255, AZUL1[0] + random.randint(-3, 3))), 
                        max(0, min(255, AZUL1[1] + random.randint(-3, 3))), 
                        max(0, min(255, AZUL1[2] + random.randint(-2, 2))))
            pygame.draw.circle(tile, color_var, (x, y), 1)
    elif variant == 1:  # Agua media
        tile.fill(AZUL2)
        # Variaciones sutiles
        for i in range(2):
            x = random.randint(0, TILE_SIZE)
            y = random.randint(0, TILE_SIZE)
            color_var = (max(0, min(255, AZUL2[0] + random.randint(-3, 3))), 
                        max(0, min(255, AZUL2[1] + random.randint(-3, 3))), 
                        max(0, min(255, AZUL2[2] + random.randint(-2, 2))))
            pygame.draw.circle(tile, color_var, (x, y), 1)
    elif variant == 2:  # Agua profunda
        tile.fill((25, 75, 115))
        # Variaciones sutiles
        for i in range(2):
            x = random.randint(0, TILE_SIZE)
            y = random.randint(0, TILE_SIZE)
            color_var = (max(0, min(255, 25 + random.randint(-3, 3))), 
                        max(0, min(255, 75 + random.randint(-3, 3))), 
                        max(0, min(255, 115 + random.randint(-2, 2))))
            pygame.draw.circle(tile, color_var, (x, y), 1)
    elif variant == 3:  # Turbulencia integrada
        # Base de agua con tinte amarillito
        base_color = (min(255, AZUL1[0] + 40), min(255, AZUL1[1] + 30), min(255, AZUL1[2] + 20))
        tile.fill(base_color)
        # Agregar turbulencia sutil
        for i in range(4):
            x = random.randint(2, TILE_SIZE-2)
            y = random.randint(2, TILE_SIZE-2)
            turb_color = (255, 231, 161)  # #ffe7a1
            pygame.draw.circle(tile, turb_color, (x, y), random.randint(2, 4))
    
    return tile

def create_shore_tile(direction):
    """Crea tiles de orilla orgánicos"""
    tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
    
    if direction == "top":  # Agua arriba, tierra abajo
        tile.fill(VERDE)
        # Orilla irregular
        points = [(0, TILE_SIZE//2 + random.randint(-3, 3))]
        for x in range(0, TILE_SIZE, 4):
            y = TILE_SIZE//2 + random.randint(-4, 4)
            points.append((x, y))
        points.append((TILE_SIZE, TILE_SIZE//2 + random.randint(-3, 3)))
        points.extend([(TILE_SIZE, 0), (0, 0)])
        pygame.draw.polygon(tile, AZUL1, points)
    elif direction == "bottom":  # Tierra arriba, agua abajo
        tile.fill(VERDE)
        points = [(0, TILE_SIZE//2 + random.randint(-3, 3))]
        for x in range(0, TILE_SIZE, 4):
            y = TILE_SIZE//2 + random.randint(-4, 4)
            points.append((x, y))
        points.append((TILE_SIZE, TILE_SIZE//2 + random.randint(-3, 3)))
        points.extend([(TILE_SIZE, TILE_SIZE), (0, TILE_SIZE)])
        pygame.draw.polygon(tile, AZUL1, points)
    elif direction == "left":  # Agua izquierda, tierra derecha
        tile.fill(VERDE)
        points = [(TILE_SIZE//2 + random.randint(-3, 3), 0)]
        for y in range(0, TILE_SIZE, 4):
            x = TILE_SIZE//2 + random.randint(-4, 4)
            points.append((x, y))
        points.append((TILE_SIZE//2 + random.randint(-3, 3), TILE_SIZE))
        points.extend([(0, TILE_SIZE), (0, 0)])
        pygame.draw.polygon(tile, AZUL1, points)
    elif direction == "right":  # Tierra izquierda, agua derecha
        tile.fill(VERDE)
        points = [(TILE_SIZE//2 + random.randint(-3, 3), 0)]
        for y in range(0, TILE_SIZE, 4):
            x = TILE_SIZE//2 + random.randint(-4, 4)
            points.append((x, y))
        points.append((TILE_SIZE//2 + random.randint(-3, 3), TILE_SIZE))
        points.extend([(TILE_SIZE, TILE_SIZE), (TILE_SIZE, 0)])
        pygame.draw.polygon(tile, AZUL1, points)
    
    return tile

def create_grass_tile(variant=0):
    """Crea tiles de pasto"""
    tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
    
    if variant == 0:
        tile.fill(VERDE)
    else:
        tile.fill(random.choice(SELVAS))
        # Agregar detalles de pasto
        for _ in range(5):
            x = random.randint(2, TILE_SIZE-2)
            y = random.randint(2, TILE_SIZE-2)
            pygame.draw.circle(tile, VERDE, (x, y), 2)
    
    return tile

def load_custom_tiles():
    """Carga tiles personalizados desde archivos PNG"""
    import os
    tiles = {}
    
    base_path = "/Users/usr011582/Documents/caida de mercurio/caida-de-mercurio-main/assets/images/"
    
    # Lista ordenada: 1 (base), 2,3,13,14,15 (con sombra), 37 (prueba)
    water_tiles = ['Map_tile_01.png', 'Map_tile_02.png', 'Map_tile_03.png', 
                   'Map_tile_13.png', 'Map_tile_14.png', 'Map_tile_15.png', 'Map_tile_37.png']
    
    try:
        # Cargar todos los tiles de agua
        loaded_water_tiles = []
        for tile_name in water_tiles:
            tile_path = base_path + tile_name
            if os.path.exists(tile_path):
                water_tile = pygame.image.load(tile_path)
                water_tile = pygame.transform.scale(water_tile, (TILE_SIZE, TILE_SIZE))
                loaded_water_tiles.append(water_tile)
        
        # Asignar tiles según tu especificación
        if loaded_water_tiles:
            # Tile 1 como base principal
            tiles['water_base'] = loaded_water_tiles[0]  # Map_tile_01
            
            # Tiles con sombra (2,3,13,14,15) para grupos ocasionales
            tiles['water_shadow_1'] = loaded_water_tiles[1] if len(loaded_water_tiles) > 1 else loaded_water_tiles[0]  # Map_tile_02
            tiles['water_shadow_2'] = loaded_water_tiles[2] if len(loaded_water_tiles) > 2 else loaded_water_tiles[0]  # Map_tile_03
            tiles['water_shadow_3'] = loaded_water_tiles[3] if len(loaded_water_tiles) > 3 else loaded_water_tiles[0]  # Map_tile_13
            tiles['water_shadow_4'] = loaded_water_tiles[4] if len(loaded_water_tiles) > 4 else loaded_water_tiles[0]  # Map_tile_14
            tiles['water_shadow_5'] = loaded_water_tiles[5] if len(loaded_water_tiles) > 5 else loaded_water_tiles[0]  # Map_tile_15
            tiles['tile_37'] = loaded_water_tiles[6] if len(loaded_water_tiles) > 6 else loaded_water_tiles[0]  # Map_tile_37
            
            # Para compatibilidad con el código existente
            tiles['water_0'] = tiles['water_base']
            tiles['water_1'] = tiles['water_base']
            tiles['water_2'] = tiles['water_base']
        
        # Usar tiles generados para orillas
        tiles['shore_top'] = create_shore_tile("top")
        tiles['shore_bottom'] = create_shore_tile("bottom")
        tiles['shore_left'] = create_shore_tile("left")
        tiles['shore_right'] = create_shore_tile("right")
        
        # Cargar tile de turbulencia (usar tile 37 en lugar de 98)
        turbulence_path = base_path + "Map_tile_37.png"
        if os.path.exists(turbulence_path):
            turbulence_tile = pygame.image.load(turbulence_path)
            turbulence_tile = pygame.transform.scale(turbulence_tile, (TILE_SIZE, TILE_SIZE))
            tiles['turbulence'] = turbulence_tile
        else:
            tiles['turbulence'] = create_water_tile(3)
        

        
    except Exception as e:

        # Si no se pueden cargar, usar tiles generados
        tiles['water_0'] = create_water_tile(0)
        tiles['water_1'] = create_water_tile(1)
        tiles['water_2'] = create_water_tile(2)
        tiles['turbulence'] = create_water_tile(3)
        tiles['shore_top'] = create_shore_tile("top")
        tiles['shore_bottom'] = create_shore_tile("bottom")
        tiles['shore_left'] = create_shore_tile("left")
        tiles['shore_right'] = create_shore_tile("right")
    
    # Tiles de pasto (generados)
    tiles['grass_0'] = create_grass_tile(0)
    tiles['grass_1'] = create_grass_tile(1)
    
    return tiles

def generate_all_tiles():
    """Genera todos los tiles"""
    return load_custom_tiles()

def save_tiles_as_images():
    """Guarda los tiles como imágenes PNG"""
    tiles = generate_all_tiles()
    tiles_dir = "/Users/usr011582/Documents/caida de mercurio/caida-de-mercurio-main/assets/tiles"
    
    if not os.path.exists(tiles_dir):
        os.makedirs(tiles_dir)
    
    for name, tile in tiles.items():
        pygame.image.save(tile, os.path.join(tiles_dir, f"{name}.png"))
    
    print(f"Tiles guardados en {tiles_dir}")
    return tiles