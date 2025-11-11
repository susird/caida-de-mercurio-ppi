import pygame
import random
import math
from utils.fish_sprites import create_fish_sprite
from config.game_config import FISH_TYPES

class Fish:
    VIBRANT_COLORS = [
        (255, 215, 0), (255, 165, 0), (0, 255, 255), (255, 20, 147),
        (50, 205, 50), (255, 69, 0), (138, 43, 226), (255, 140, 0)
    ]
    
    def __init__(self, x, y, fish_type="normal"):
        self.x = float(x)
        self.y = float(y)
        self.fish_type = fish_type
        self.direction = random.uniform(0, 2 * math.pi)
        self.time = random.uniform(0, 100)
        
        self._setup_properties()
        self._create_sprites()
    
    def _setup_properties(self):
        self.color = random.choice(self.VIBRANT_COLORS)
        self.size = random.randint(18, 24)
        
        fish_config = FISH_TYPES[self.fish_type]
        self.fish_name = random.choice(fish_config["names"])
        self.speed = random.uniform(*fish_config["speed_range"])
        self.mercury_damage = fish_config["health_effect"]
        self.score_value = fish_config["score_value"]
    
    def _create_sprites(self):
        self.sprite = create_fish_sprite(self.color, self.size)
        self.flipped_sprite = pygame.transform.flip(self.sprite, True, False)
    
    def update(self, tile_map):
        self.time += 0.1
        
        speed_variation = self._calculate_speed_variation()
        new_x, new_y = self._calculate_new_position(speed_variation)
        
        if self._is_valid_position(new_x, new_y, tile_map):
            self.x = new_x
            self.y = new_y
        else:
            self._change_direction()
        
        if random.random() < 0.01:
            self.direction += random.uniform(-0.5, 0.5)
    
    def _calculate_speed_variation(self):
        if self.fish_type == "high_mercury":
            return 0.7 + 0.6 * math.sin(self.time * 2)
        elif self.fish_type == "good":
            return 1.2 + 0.3 * math.sin(self.time * 3)
        return 1.0
    
    def _calculate_new_position(self, speed_variation):
        effective_speed = self.speed * speed_variation
        new_x = self.x + math.cos(self.direction) * effective_speed
        new_y = self.y + math.sin(self.direction) * effective_speed + math.sin(self.time) * 0.3
        return new_x, new_y
    
    def _is_valid_position(self, x, y, tile_map):
        from core.settings import MAP_ANCHO, MAP_ALTO
        if not (0 < x < MAP_ANCHO and 0 < y < MAP_ALTO):
            return False
        tile_type = tile_map.get_tile_at_pixel(x, y)
        return tile_map.is_water_tile(tile_type)
    
    def _change_direction(self):
        self.direction += random.uniform(1.5, 4.5)
    
    def draw(self, surface, cam_x, cam_y):
        screen_x = int(self.x - cam_x)
        screen_y = int(self.y - cam_y)
        
        if not self._is_on_screen(screen_x, screen_y, surface):
            return
        
        sprite = self.flipped_sprite if math.cos(self.direction) < 0 else self.sprite
        sprite_rect = sprite.get_rect(center=(screen_x, screen_y))
        surface.blit(sprite, sprite_rect)
    
    def _is_on_screen(self, screen_x, screen_y, surface):
        return (-30 <= screen_x <= surface.get_width() + 30 and 
                -30 <= screen_y <= surface.get_height() + 30)