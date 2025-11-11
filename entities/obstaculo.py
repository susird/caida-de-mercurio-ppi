import pygame
import random
import math
from pathlib import Path
from config.settings import IMAGES_DIR

class Obstaculo:
    OBSTACLE_CONFIG = {
        "barril": {"file": "barril.png", "size": (50, 40), "color": (101, 67, 33)},
        "tronco": {"file": "tronco.png", "size": (90, 70), "color": (139, 69, 19)}
    }
    
    def __init__(self, x, y, tipo="tronco"):
        self.x = float(x)
        self.y = float(y)
        self.tipo = tipo
        self.direction = math.pi / 2 + random.uniform(-0.3, 0.3)
        self.base_speed = random.uniform(2.0, 4.0)
        self.speed = self.base_speed
        self.time = random.uniform(0, 100)
        
        self.sprite = self._load_sprite()
    
    def _load_sprite(self):
        config = self.OBSTACLE_CONFIG.get(self.tipo, self.OBSTACLE_CONFIG["tronco"])
        sprite_path = Path(IMAGES_DIR) / config["file"]
        
        try:
            if sprite_path.exists():
                original_sprite = pygame.image.load(str(sprite_path))
                return pygame.transform.scale(original_sprite, config["size"])
        except pygame.error:
            pass
        
        return self._create_fallback_sprite(config)
    
    def _create_fallback_sprite(self, config):
        sprite = pygame.Surface(config["size"])
        sprite.fill(config["color"])
        return sprite
    
    def update(self, tile_map, player_y=0, fish_collected=0):
        self.time += 0.1
        self._update_speed(player_y, fish_collected)
        
        new_x, new_y = self._calculate_new_position()
        
        if self._is_valid_position(new_x, new_y, tile_map):
            self.x = new_x
            self.y = new_y
        elif self._is_out_of_bounds(new_y):
            self._respawn(tile_map)
        else:
            self._correct_position(new_y, tile_map)
    
    def _update_speed(self, player_y, fish_collected=0):
        from core.settings import MAP_ALTO
        progress = player_y / MAP_ALTO
        
        # Multiplicador base por progreso
        speed_multiplier = 1 + (progress * 2)
        
        # Multiplicador adicional por peces recolectados
        if fish_collected >= 15:
            speed_multiplier *= 2.5  # Mucho más rápido
        elif fish_collected >= 10:
            speed_multiplier *= 1.8  # Más rápido
        
        self.speed = self.base_speed * speed_multiplier
    
    def _calculate_new_position(self):
        lateral_drift = 0.3 * math.sin(self.time * 0.5)
        new_x = self.x + lateral_drift
        new_y = self.y + self.speed
        return new_x, new_y
    
    def _is_valid_position(self, x, y, tile_map):
        from core.settings import MAP_ANCHO, MAP_ALTO
        if not (0 < x < MAP_ANCHO and 0 < y < MAP_ALTO):
            return False
        tile_type = tile_map.get_tile_at_pixel(x, y)
        return tile_map.is_water_tile(tile_type)
    
    def _is_out_of_bounds(self, y):
        from core.settings import MAP_ALTO
        return y >= MAP_ALTO
    
    def _correct_position(self, new_y, tile_map):
        from core.settings import MAP_ANCHO
        self.y = new_y
        
        for offset in [-20, -10, 10, 20, -30, 30]:
            test_x = self.x + offset
            if (0 < test_x < MAP_ANCHO and 
                tile_map.is_water_tile(tile_map.get_tile_at_pixel(test_x, new_y))):
                self.x = test_x
                break
    
    def _respawn(self, tile_map):
        spawn_side = random.choice(['top', 'left', 'right'])
        
        if spawn_side == 'top':
            self._respawn_from_top(tile_map)
        elif spawn_side == 'left':
            self._respawn_from_left(tile_map)
        else:
            self._respawn_from_right(tile_map)
    
    def _respawn_from_top(self, tile_map):
        from core.settings import MAP_ANCHO
        self.y = -50
        for _ in range(100):
            test_x = random.randint(100, MAP_ANCHO - 100)
            if tile_map.is_water_tile(tile_map.get_tile_at_pixel(test_x, 100)):
                self.x = test_x
                break
    
    def _respawn_from_left(self, tile_map):
        from core.settings import MAP_ALTO
        self.x = -50
        for _ in range(100):
            test_y = random.randint(100, MAP_ALTO - 100)
            if tile_map.is_water_tile(tile_map.get_tile_at_pixel(100, test_y)):
                self.y = test_y
                break
    
    def _respawn_from_right(self, tile_map):
        from core.settings import MAP_ANCHO, MAP_ALTO
        self.x = MAP_ANCHO + 50
        for _ in range(100):
            test_y = random.randint(100, MAP_ALTO - 100)
            if tile_map.is_water_tile(tile_map.get_tile_at_pixel(MAP_ANCHO - 100, test_y)):
                self.y = test_y
                break
    
    def draw(self, surface, cam_x, cam_y, tile_map):
        screen_x = int(self.x - cam_x)
        screen_y = int(self.y - cam_y)
        
        if (self._is_on_screen(screen_x, screen_y, surface) and
            tile_map.is_water_tile(tile_map.get_tile_at_pixel(self.x, self.y))):
            sprite_rect = self.sprite.get_rect(center=(screen_x, screen_y))
            surface.blit(self.sprite, sprite_rect)
    
    def _is_on_screen(self, screen_x, screen_y, surface):
        return (-50 <= screen_x <= surface.get_width() + 50 and 
                -50 <= screen_y <= surface.get_height() + 50)
    
    def collides_with_player(self, player_x, player_y, player_radius=30):
        obstacle_radius = max(self.sprite.get_width(), self.sprite.get_height()) // 3
        
        dx = self.x - player_x
        dy = self.y - player_y
        distance = math.sqrt(dx * dx + dy * dy)
        
        return distance < (player_radius + obstacle_radius)