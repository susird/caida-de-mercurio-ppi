# utils/jungle_sprites.py
import pygame
import random
import math

def create_bush_sprite(size=12):
    """Crea un sprite de arbusto"""
    bush = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Arbusto con múltiples tonos de verde
    bush_colors = [
        (34, 139, 34), (0, 100, 0), (46, 125, 50), (85, 107, 47),
        (107, 142, 35), (60, 179, 113), (0, 128, 0), (50, 205, 50),
        (124, 252, 0), (0, 250, 154), (32, 178, 170), (0, 201, 87)
    ]
    bush_color = random.choice(bush_colors)
    
    # Círculos superpuestos para forma orgánica
    for i in range(3):
        x = size // 2 + random.randint(-3, 3)
        y = size // 2 + random.randint(-2, 2)
        radius = random.randint(size//4, size//3)
        pygame.draw.circle(bush, bush_color, (x, y), radius)
    
    return bush

def create_bird_sprite(size=8):
    """Crea un sprite de ave"""
    bird = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Colores de aves tropicales
    bird_colors = [(255, 0, 0), (255, 255, 0), (0, 191, 255), (255, 20, 147), (50, 205, 50)]
    bird_color = random.choice(bird_colors)
    
    # Cuerpo del ave (elipse pequeña)
    body_rect = pygame.Rect(size//4, size//2, size//2, size//4)
    pygame.draw.ellipse(bird, bird_color, body_rect)
    
    # Alas (líneas)
    wing_color = (max(0, bird_color[0]-30), max(0, bird_color[1]-30), max(0, bird_color[2]-30))
    pygame.draw.line(bird, wing_color, (size//4, size//2), (0, size//3), 2)
    pygame.draw.line(bird, wing_color, (3*size//4, size//2), (size, size//3), 2)
    
    return bird

def create_flower_sprite(size=6):
    """Crea un sprite de flor"""
    flower = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Colores de flores tropicales
    flower_colors = [(255, 20, 147), (255, 69, 0), (255, 215, 0), (138, 43, 226)]
    flower_color = random.choice(flower_colors)
    
    # Pétalos (círculos pequeños alrededor del centro)
    center_x, center_y = size // 2, size // 2
    for angle in range(0, 360, 60):
        petal_x = center_x + int(2 * math.cos(math.radians(angle)))
        petal_y = center_y + int(2 * math.sin(math.radians(angle)))
        pygame.draw.circle(flower, flower_color, (petal_x, petal_y), 2)
    
    # Centro de la flor
    pygame.draw.circle(flower, (255, 255, 0), (center_x, center_y), 1)
    
    return flower

def create_vine_sprite(size=15):
    """Crea un sprite de enredadera"""
    vine = pygame.Surface((size, size), pygame.SRCALPHA)
    
    vine_color = (34, 139, 34)
    # Líneas curvas para simular enredaderas
    for i in range(3):
        start_x = random.randint(0, size//2)
        start_y = 0
        end_x = random.randint(size//2, size)
        end_y = size
        pygame.draw.line(vine, vine_color, (start_x, start_y), (end_x, end_y), 2)
    
    return vine

def create_mushroom_sprite(size=8):
    """Crea un sprite de hongo"""
    mushroom = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Tallo
    stalk_color = (245, 245, 220)
    pygame.draw.rect(mushroom, stalk_color, (size//2-1, size//2, 2, size//2))
    
    # Sombrero
    cap_colors = [(255, 0, 0), (255, 165, 0), (139, 69, 19), (160, 82, 45)]
    cap_color = random.choice(cap_colors)
    pygame.draw.circle(mushroom, cap_color, (size//2, size//2), size//3)
    
    # Puntos en el sombrero
    if random.random() < 0.5:
        pygame.draw.circle(mushroom, (255, 255, 255), (size//2-2, size//2-1), 1)
        pygame.draw.circle(mushroom, (255, 255, 255), (size//2+1, size//2-2), 1)
    
    return mushroom

def create_butterfly_sprite(size=6):
    """Crea un sprite de mariposa"""
    butterfly = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Colores de mariposas tropicales
    wing_colors = [(255, 20, 147), (0, 191, 255), (255, 215, 0), (138, 43, 226), (255, 69, 0)]
    wing_color = random.choice(wing_colors)
    
    # Cuerpo
    pygame.draw.line(butterfly, (0, 0, 0), (size//2, 1), (size//2, size-1), 1)
    
    # Alas
    pygame.draw.circle(butterfly, wing_color, (size//2-2, size//3), 2)
    pygame.draw.circle(butterfly, wing_color, (size//2+2, size//3), 2)
    pygame.draw.circle(butterfly, wing_color, (size//2-2, 2*size//3), 1)
    pygame.draw.circle(butterfly, wing_color, (size//2+2, 2*size//3), 1)
    
    return butterfly

class JungleElement:
    def __init__(self, x, y, element_type, sprite):
        self.x = x
        self.y = y
        self.type = element_type
        self.sprite = sprite
        self.animation_offset = random.uniform(0, 100)
        
    def update(self):
        self.animation_offset += 0.02
        
    def draw(self, surface, cam_x, cam_y):
        screen_x = int(self.x - cam_x)
        screen_y = int(self.y - cam_y)
        
        # Solo dibujar si está en pantalla
        if -50 <= screen_x <= surface.get_width() + 50 and -50 <= screen_y <= surface.get_height() + 50:
            # Animación sutil para aves y flores
            if self.type == 'bird':
                offset_y = int(2 * math.sin(self.animation_offset))
                screen_y += offset_y
            elif self.type == 'flower':
                offset_x = int(1 * math.sin(self.animation_offset * 0.5))
                screen_x += offset_x
                
            sprite_rect = self.sprite.get_rect(center=(screen_x, screen_y))
            surface.blit(self.sprite, sprite_rect)