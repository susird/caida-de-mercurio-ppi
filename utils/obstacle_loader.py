# utils/obstacle_loader.py
import pygame
import os
import random

def load_obstacle_tiles():
    """Carga tiles de obstáculos para el agua"""
    obstacle_tiles = []
    base_path = "/Users/usr011582/Documents/caida de mercurio/caida-de-mercurio-main/assets/images/"
    
    # Cargar barril y tronco
    obstacles = ['barril.png', 'tronco.png']
    
    for obstacle_file in obstacles:
        obstacle_path = base_path + obstacle_file
        if os.path.exists(obstacle_path):
            try:
                obstacle_tile = pygame.image.load(obstacle_path)
                # Diferentes tamaños para variedad
                for scale in [0.8, 1.0, 1.2]:
                    size = int(32 * scale)
                    scaled_obstacle = pygame.transform.scale(obstacle_tile, (size, size))
                    obstacle_tiles.append(scaled_obstacle)
            except:
                print(f"Error cargando {obstacle_path}")
    
    return obstacle_tiles

class Obstacle:
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.rect = pygame.Rect(x - sprite.get_width()//2, y - sprite.get_height()//2, 
                               sprite.get_width(), sprite.get_height())
        
    def draw(self, surface, cam_x, cam_y):
        screen_x = int(self.x - cam_x)
        screen_y = int(self.y - cam_y)
        
        # Solo dibujar si está en pantalla
        if -50 <= screen_x <= surface.get_width() + 50 and -50 <= screen_y <= surface.get_height() + 50:
            sprite_rect = self.sprite.get_rect(center=(screen_x, screen_y))
            surface.blit(self.sprite, sprite_rect)
    
    def collides_with_player(self, player_x, player_y, player_radius=25):
        """Verifica colisión con el jugador"""
        player_rect = pygame.Rect(player_x - player_radius, player_y - player_radius, 
                                 player_radius * 2, player_radius * 2)
        return self.rect.colliderect(player_rect)