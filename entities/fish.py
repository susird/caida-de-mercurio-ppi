# entities/fish.py
import pygame
import random
import math
from utils.fish_sprites import create_fish_sprite, get_fish_colors

class Fish:
    def __init__(self, x, y, fish_type="normal"):
        self.x = float(x)
        self.y = float(y)
        self.fish_type = fish_type
        self.setup_fish_properties()
        self.direction = random.uniform(0, 2 * math.pi)
        self.time = random.uniform(0, 100)
        # Crear sprite del pez
        self.sprite = create_fish_sprite(self.color, self.size)
        self.flipped_sprite = pygame.transform.flip(self.sprite, True, False)
    
    def setup_fish_properties(self):
        """Configura las propiedades según el tipo de pez"""
        # Colores aleatorios vivos para todos los peces
        colores_vivos = [
            (255, 215, 0),   # Dorado
            (255, 165, 0),   # Naranja
            (0, 255, 255),   # Cian
            (255, 20, 147),  # Rosa fuerte
            (50, 205, 50),   # Verde lima
            (255, 69, 0),    # Rojo naranja
            (138, 43, 226),  # Violeta
            (255, 140, 0),   # Naranja oscuro
        ]
        self.color = random.choice(colores_vivos)
        self.size = random.randint(18, 24)  # Tamaño similar
        
        if self.fish_type == "good":
            # Peces buenos - RÁPIDOS
            fish_data = random.choice([
                "Bocachico", "Mojarra", "Sábalo", "Cucha"
            ])
            self.fish_name = fish_data
            self.speed = random.uniform(1.2, 1.8)  # MUY RÁPIDOS
            self.mercury_damage = -2  # Recuperación
        else:
            # Peces malos (normal y high_mercury) - LENTOS
            fish_data = random.choice([
                "Tucunaré", "Bagre", "Dorado", "Moncholo"
            ])
            self.fish_name = fish_data
            self.speed = random.uniform(0.3, 0.6)  # LENTOS
            if self.fish_type == "high_mercury":
                self.mercury_damage = 4
            else:
                self.mercury_damage = 2
    
    def update(self, tile_map):
        self.time += 0.1
        
        # Movimiento errático para peces con mucho mercurio
        speed_variation = 1.0
        if self.fish_type == "high_mercury":
            speed_variation = 0.7 + 0.6 * math.sin(self.time * 2)  # Movimiento errático
        elif self.fish_type == "good":
            speed_variation = 1.2 + 0.3 * math.sin(self.time * 3)  # Movimiento ágil
        
        # Calcular nueva posición
        effective_speed = self.speed * speed_variation
        new_x = self.x + math.cos(self.direction) * effective_speed
        new_y = self.y + math.sin(self.direction) * effective_speed + math.sin(self.time) * 0.3
        
        # Verificar si la nueva posición está en agua
        from core.settings import MAP_ANCHO, MAP_ALTO
        if (0 < new_x < MAP_ANCHO and 0 < new_y < MAP_ALTO):
            tile_type = tile_map.get_tile_at_pixel(new_x, new_y)
            if tile_map.is_water_tile(tile_type):
                self.x = new_x
                self.y = new_y
            else:
                # Cambiar dirección si va hacia tierra
                self.direction += random.uniform(1.5, 4.5)
        else:
            # Cambiar dirección si va fuera del mapa
            self.direction += random.uniform(1.5, 4.5)
        
        # Cambiar dirección ocasionalmente
        if random.random() < 0.01:
            self.direction += random.uniform(-0.5, 0.5)
    
    def draw(self, surface, cam_x, cam_y):
        screen_x = int(self.x - cam_x)
        screen_y = int(self.y - cam_y)
        # Solo dibujar si está en pantalla
        if -30 <= screen_x <= surface.get_width() + 30 and -30 <= screen_y <= surface.get_height() + 30:
            # Elegir sprite según dirección
            sprite_to_use = self.flipped_sprite if math.cos(self.direction) < 0 else self.sprite
            # Centrar el sprite
            sprite_rect = sprite_to_use.get_rect(center=(screen_x, screen_y))
            surface.blit(sprite_to_use, sprite_rect)