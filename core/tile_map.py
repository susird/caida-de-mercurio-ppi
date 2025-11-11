# core/tile_map.py
import pygame
import random
import math
from utils.tile_generator import generate_all_tiles, TILE_SIZE
from utils.jungle_sprites import create_bush_sprite, create_bird_sprite, create_flower_sprite, create_vine_sprite, create_mushroom_sprite, create_butterfly_sprite, JungleElement
from utils.tree_loader import load_tree_tiles, load_bush_tiles, load_flower_tiles, load_rock_tiles, VegetationElement
from utils.obstacle_loader import load_obstacle_tiles, Obstacle
from core.settings import MAP_ANCHO, MAP_ALTO

class TileMap:
    def __init__(self, seed=None):
        if seed:
            random.seed(seed)
        self.tiles = generate_all_tiles()
        self.map_width = MAP_ANCHO // TILE_SIZE
        self.map_height = MAP_ALTO // TILE_SIZE
        self.tile_grid = []
        self.jungle_elements = []
        self.tree_elements = []
        self.bush_elements = []
        self.flower_elements = []
        self.rock_elements = []
        self.obstacles = []
        self.tree_tiles = load_tree_tiles()
        self.bush_tiles = load_bush_tiles()
        self.flower_tiles = load_flower_tiles()
        self.rock_tiles = load_rock_tiles()
        self.obstacle_tiles = load_obstacle_tiles()
        self.generate_river_map()
        self.generate_jungle()
    
    def generate_river_map(self):
        """Genera un mapa de río usando tiles"""
        # Inicializar con pasto
        self.tile_grid = [['grass_0' for _ in range(self.map_width)] for _ in range(self.map_height)]
        
        # Crear río serpenteante más grande
        river_center = self.map_width // 2
        river_width = 15  # tiles de ancho (un tris más pequeño)
        
        # Generar río más recto con curvas pequeñas
        base_center = self.map_width // 2
        
        for y in range(self.map_height):
            # Curvas pequeñas y suaves
            small_curve = 3 * math.sin(y * 0.05)
            
            # Curva secundaria muy sutil
            tiny_curve = 2 * math.sin(y * 0.12 + 1.0)
            
            # Variación mínima aleatoria
            random_variation = random.randint(-1, 1) if y % 10 == 0 else 0
            
            # Calcular posición final del centro del río
            river_center = int(base_center + small_curve + tiny_curve + random_variation)
            river_center = max(river_width//2, min(self.map_width - river_width//2, river_center))
            
            # Colocar tiles de agua con sombras directamente
            shadow_tiles = ['water_shadow_1', 'water_shadow_2', 'water_shadow_3', 'water_shadow_4', 'water_shadow_5']
            
            for x in range(max(0, river_center - river_width//2), 
                          min(self.map_width, river_center + river_width//2)):
                # Usar tiles sombreados para TODO el río
                shadow_tile = random.choice(shadow_tiles)
                self.tile_grid[y][x] = shadow_tile
        
        # Agregar turbulencias de forma más natural
        for y in range(0, self.map_height, 15):  # Cada 15 tiles
            # Buscar el centro del río en esta fila
            water_tiles = []
            for x in range(self.map_width):
                if y < self.map_height and self.is_water_tile(self.tile_grid[y][x]):
                    water_tiles.append(x)
            
            if len(water_tiles) > 4:  # Solo si hay suficiente río
                # Crear 1-2 zonas de turbulencia en esta sección
                for _ in range(random.randint(1, 2)):
                    center_x = random.choice(water_tiles[1:-1])  # No en los bordes
                    # Crear zona de turbulencia 6x6 mucho más grande
                    for dy in range(6):
                        for dx in range(6):
                            ty, tx = y + dy, center_x + dx - 3
                            if (0 <= ty < self.map_height and 0 <= tx < self.map_width and 
                                self.is_water_tile(self.tile_grid[ty][tx])):
                                self.tile_grid[ty][tx] = 'turbulence'
    
    def generate_jungle(self):
        """Genera elementos de selva en las zonas de tierra sin superposiciones"""
        # Crear grid de ocupación para evitar superposiciones
        grid_size = 25  # Tamaño de celda más pequeño para más densidad
        occupied_grid = set()
        
        def is_position_free(x, y, radius=25):
            """Verifica si una posición está libre en el grid"""
            grid_x = x // grid_size
            grid_y = y // grid_size
            # Verificar celdas adyacentes
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if (grid_x + dx, grid_y + dy) in occupied_grid:
                        return False
            return True
        
        def occupy_position(x, y):
            """Marca una posición como ocupada"""
            grid_x = x // grid_size
            grid_y = y // grid_size
            occupied_grid.add((grid_x, grid_y))
        
        # Generar rocas primero (elementos base) - muy pocas
        for _ in range(800):  # Muy pocas rocas
            x = random.randint(0, MAP_ANCHO)
            y = random.randint(0, MAP_ALTO)
            
            tile_type = self.get_tile_at_pixel(x, y)
            if (not self.is_water_tile(tile_type) and self.rock_tiles and 
                is_position_free(x, y)):
                rock_sprite = random.choice(self.rock_tiles)
                self.rock_elements.append(VegetationElement(x, y, rock_sprite))
                occupy_position(x, y)
        
        # Generar árboles (ULTRA MEGA cantidad!)
        for _ in range(80000):  # ULTRA MEGA cantidad de árboles
            x = random.randint(0, MAP_ANCHO)
            y = random.randint(0, MAP_ALTO)
            
            tile_type = self.get_tile_at_pixel(x, y)
            if (not self.is_water_tile(tile_type) and self.tree_tiles and 
                is_position_free(x, y)):
                tree_sprite = random.choice(self.tree_tiles)
                self.tree_elements.append(VegetationElement(x, y, tree_sprite))
                occupy_position(x, y)
        
        # Generar arbustos (elementos medianos)
        for _ in range(10000):  # Reducido
            x = random.randint(0, MAP_ANCHO)
            y = random.randint(0, MAP_ALTO)
            
            tile_type = self.get_tile_at_pixel(x, y)
            if (not self.is_water_tile(tile_type) and self.bush_tiles and 
                is_position_free(x, y, radius=15)):  # Radio menor para arbustos
                bush_sprite = random.choice(self.bush_tiles)
                self.bush_elements.append(VegetationElement(x, y, bush_sprite))
                # No ocupar grid para arbustos (pueden estar cerca de otros elementos)
        
        # Generar flores (muchas más florecitas!)
        for _ in range(5000):
            x = random.randint(0, MAP_ANCHO)
            y = random.randint(0, MAP_ALTO)
            
            tile_type = self.get_tile_at_pixel(x, y)
            if not self.is_water_tile(tile_type) and self.flower_tiles:
                flower_sprite = random.choice(self.flower_tiles)
                self.flower_elements.append(VegetationElement(x, y, flower_sprite))
                # No ocupar grid para flores
        
        # No generar obstáculos estáticos aquí, se generan dinámicos en game.py
        pass
    
    def update_jungle(self):
        """Actualiza animaciones de la selva"""
        for element in self.jungle_elements:
            element.update()
    
    def get_tile_at_pixel(self, x, y):
        """Obtiene el tipo de tile en una posición de píxel"""
        tile_x = int(x // TILE_SIZE)
        tile_y = int(y // TILE_SIZE)
        
        if 0 <= tile_x < self.map_width and 0 <= tile_y < self.map_height:
            return self.tile_grid[tile_y][tile_x]
        return 'grass_0'
    
    def is_water_tile(self, tile_type):
        """Verifica si un tile es de agua"""
        return (tile_type.startswith('water_') or 
                tile_type == 'turbulence' or 
                tile_type == 'water_base' or 
                tile_type == 'tile_37')
    
    def is_turbulence_tile(self, tile_type):
        """Verifica si un tile es de turbulencia"""
        return tile_type == 'turbulence'
    
    def render(self, surface, cam_x, cam_y):
        """Renderiza el mapa de tiles y elementos de selva"""
        # Calcular qué tiles están visibles
        start_x = max(0, cam_x // TILE_SIZE)
        start_y = max(0, cam_y // TILE_SIZE)
        end_x = min(self.map_width, (cam_x + surface.get_width()) // TILE_SIZE + 1)
        end_y = min(self.map_height, (cam_y + surface.get_height()) // TILE_SIZE + 1)
        
        # Dibujar tiles visibles
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile_type = self.tile_grid[y][x]
                tile_surface = self.tiles[tile_type]
                
                screen_x = x * TILE_SIZE - cam_x
                screen_y = y * TILE_SIZE - cam_y
                
                surface.blit(tile_surface, (screen_x, screen_y))
        
        # Dibujar árboles reales
        for tree in self.tree_elements:
            tree.draw(surface, cam_x, cam_y)
        
        # Dibujar arbustos reales
        for bush in self.bush_elements:
            bush.draw(surface, cam_x, cam_y)
        
        # Dibujar flores reales
        for flower in self.flower_elements:
            flower.draw(surface, cam_x, cam_y)
        
        # Dibujar rocas reales
        for rock in self.rock_elements:
            rock.draw(surface, cam_x, cam_y)
        
        # Dibujar obstáculos
        for obstacle in self.obstacles:
            obstacle.draw(surface, cam_x, cam_y)
        
        # Dibujar elementos de selva
        for element in self.jungle_elements:
            element.draw(surface, cam_x, cam_y)