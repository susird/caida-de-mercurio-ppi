# entities/obstaculo.py
import pygame
import random
import math
import os

class Obstaculo:
    def __init__(self, x, y, tipo="tronco"):
        self.x = float(x)
        self.y = float(y)
        self.tipo = tipo
        # Movimiento solo hacia abajo con ligera variación lateral
        self.direction = math.pi / 2 + random.uniform(-0.3, 0.3)  # Hacia abajo con variación
        self.base_speed = random.uniform(0.5, 1.0)
        self.speed = self.base_speed
        self.time = random.uniform(0, 100)
        
        # Cargar sprite según tipo
        base_path = "/Users/usr011582/Documents/caida de mercurio/caida-de-mercurio-main/assets/images/"
        
        if tipo == "barril":
            sprite_path = base_path + "barril.png"
        else:  # tronco por defecto
            sprite_path = base_path + "tronco.png"
        
        if os.path.exists(sprite_path):
            original_sprite = pygame.image.load(sprite_path)
            # Tamaños similares al personaje
            if tipo == "barril":
                new_size = (50, 40)  # Un poco más pequeño
            else:  # tronco
                new_size = (90, 70)  # Mismo tamaño que el personaje
            self.sprite = pygame.transform.scale(original_sprite, new_size)
        else:
            # Sprite de respaldo
            size = 60 if tipo == "barril" else 80
            self.sprite = pygame.Surface((size, size))
            color = (139, 69, 19) if tipo == "tronco" else (101, 67, 33)
            self.sprite.fill(color)
    
    def update(self, tile_map, player_y=0):
        self.time += 0.1
        
        # Aumentar velocidad según progreso del jugador
        from core.settings import MAP_ALTO
        progreso = player_y / MAP_ALTO  # 0 a 1
        speed_multiplier = 1 + (progreso * 2)  # 1x a 3x velocidad
        self.speed = self.base_speed * speed_multiplier
        
        # Movimiento principalmente hacia abajo
        lateral_drift = 0.3 * math.sin(self.time * 0.5)  # Deriva lateral suave
        
        # Calcular nueva posición (principalmente hacia abajo)
        new_x = self.x + lateral_drift
        new_y = self.y + self.speed
        
        # Verificar si la nueva posición está en agua
        from core.settings import MAP_ANCHO, MAP_ALTO
        if (0 < new_x < MAP_ANCHO and 0 < new_y < MAP_ALTO):
            tile_type = tile_map.get_tile_at_pixel(new_x, new_y)
            if tile_map.is_water_tile(tile_type):
                self.x = new_x
                self.y = new_y
            else:
                # Si se sale del río lateralmente, corregir posición
                self.y = new_y  # Seguir bajando
                # Buscar posición válida en agua cerca
                for offset in [-20, -10, 10, 20, -30, 30]:
                    test_x = self.x + offset
                    if (0 < test_x < MAP_ANCHO and 
                        tile_map.is_water_tile(tile_map.get_tile_at_pixel(test_x, new_y))):
                        self.x = test_x
                        break
        else:
            # Si sale del mapa por abajo, reaparecer desde arriba o lados
            if new_y >= MAP_ALTO:
                # Aparecer aleatoriamente desde arriba o lados
                spawn_side = random.choice(['top', 'left', 'right'])
                
                if spawn_side == 'top':
                    self.y = -50
                    # Buscar posición en agua desde arriba
                    for _ in range(100):
                        test_x = random.randint(100, MAP_ANCHO - 100)
                        if tile_map.is_water_tile(tile_map.get_tile_at_pixel(test_x, 100)):
                            self.x = test_x
                            break
                elif spawn_side == 'left':
                    self.x = -50
                    # Buscar posición en agua desde la izquierda
                    for _ in range(100):
                        test_y = random.randint(100, MAP_ALTO - 100)
                        if tile_map.is_water_tile(tile_map.get_tile_at_pixel(100, test_y)):
                            self.y = test_y
                            break
                else:  # right
                    self.x = MAP_ANCHO + 50
                    # Buscar posición en agua desde la derecha
                    for _ in range(100):
                        test_y = random.randint(100, MAP_ALTO - 100)
                        if tile_map.is_water_tile(tile_map.get_tile_at_pixel(MAP_ANCHO - 100, test_y)):
                            self.y = test_y
                            break
    
    def draw(self, surface, cam_x, cam_y, tile_map):
        screen_x = int(self.x - cam_x)
        screen_y = int(self.y - cam_y)
        # Solo dibujar si está en pantalla y en agua
        if (-50 <= screen_x <= surface.get_width() + 50 and 
            -50 <= screen_y <= surface.get_height() + 50 and
            tile_map.is_water_tile(tile_map.get_tile_at_pixel(self.x, self.y))):
            # Centrar el sprite
            sprite_rect = self.sprite.get_rect(center=(screen_x, screen_y))
            surface.blit(self.sprite, sprite_rect)
    
    def collides_with_player(self, player_x, player_y, player_radius=30):
        """Verifica colisión con el jugador"""
        # Radio del obstáculo basado en su tamaño
        obstaculo_radius = max(self.sprite.get_width(), self.sprite.get_height()) // 3
        
        # Distancia entre centros
        dx = self.x - player_x
        dy = self.y - player_y
        distance = math.sqrt(dx * dx + dy * dy)
        
        return distance < (player_radius + obstaculo_radius)