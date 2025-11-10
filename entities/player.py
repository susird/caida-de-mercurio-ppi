# entities/player.py
import random
import pygame
from core.settings import MAP_ANCHO, MAP_ALTO, AZUL1, AZUL2, TURBULENCIA
from utils.constants import BARCO_VEL, BARCO_VEL_TURBULENCIA, BARCO_VEL_ACELERON

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = BARCO_VEL
        self.vel_turbulencia = BARCO_VEL_TURBULENCIA
        self.vel_aceleron = BARCO_VEL_ACELERON
        self.frame = 0
        self.contador_anim = 0
        self.vida = 100
        self.en_turbulencia = False
        self.mensaje_turbulencia = ""
        self.tiempo_mensaje = 0
        self.sprite_especial = False
        self.pescando = False
        self.tiempo_pescando = 0
        self.mensaje_pez = ""
        self.tiempo_mensaje_pez = 0
        self.colision_tronco = False
        self.tiempo_colision_tronco = 0
        self.mensaje_tronco = ""
        self.peces_buenos = 0
        self.peces_recolectados = 0
        self.tiempo_inicio = pygame.time.get_ticks()

    def en_agua(self, tile_map):
        """Verifica si el centro del barco está en agua"""
        if 0 <= self.x < MAP_ANCHO and 0 <= self.y < MAP_ALTO:
            tile_type = tile_map.get_tile_at_pixel(self.x, self.y)
            return tile_map.is_water_tile(tile_type)
        return False

    def dentro_turbulencia(self, tile_map):
        """Detecta si el barco está en una zona de turbulencia"""
        tile_type = tile_map.get_tile_at_pixel(self.x, self.y)
        return tile_map.is_turbulence_tile(tile_type)

    def update(self, keys, tile_map):
        """Actualiza la posición del jugador"""
        vel_actual = self.vel
        nuevo_x, nuevo_y = self.x, self.y
        movio = False  # Inicializar movio

        # Detectar si presiona S para pescar
        if keys[pygame.K_s] and not self.pescando:
            # Buscar peces cercanos
            pez_cercano = self.buscar_pez_cercano(tile_map)
            if pez_cercano:
                # Pescar el pez
                if hasattr(tile_map, 'peces_activos'):
                    tile_map.peces_activos.remove(pez_cercano)
                self.pescando = True
                # Aplicar efecto según tipo de pez
                damage = pez_cercano.mercury_damage
                fish_name = pez_cercano.fish_name
                
                if damage > 0:
                    # Pez tóxico (lento)
                    self.vida = max(0, self.vida - damage)
                    self.peces_recolectados += 1  # Los malos suman 1
                    self.mensaje_pez = f"{fish_name} -{damage} vida"
                else:
                    # Pez bueno (rápido)
                    self.vida = min(100, self.vida + abs(damage))
                    self.peces_recolectados += 2  # Los buenos suman 2
                    self.mensaje_pez = f"{fish_name} +{abs(damage)} vida"
                
                self.tiempo_mensaje_pez = 180  # 3 segundos
        
        # Actualizar mensaje de pez
        if self.tiempo_mensaje_pez > 0:
            self.tiempo_mensaje_pez -= 1
        
        # Verificar colisión con obstáculos
        if hasattr(tile_map, 'obstaculos_activos'):
            for obstaculo in tile_map.obstaculos_activos:
                if obstaculo.collides_with_player(self.x, self.y) and not self.colision_tronco:
                    # Colisión con obstáculo - verificar si está en turbulencia
                    if self.dentro_turbulencia(tile_map):
                        self.vida = max(0, self.vida - 2)
                        self.mensaje_tronco = "¡Agua tóxica! Pierdes 2 puntos de vida"
                    else:
                        self.vida = max(0, self.vida - 1)
                        self.mensaje_tronco = "¡Plaf! Pierdes 1 punto de vida"
                    self.tiempo_colision_tronco = 180  # 3 segundos
                    self.colision_tronco = True
                    self.sprite_especial = True  # Activar navegante_caido
                    break
        
        # Actualizar mensaje de tronco
        if self.tiempo_colision_tronco > 0:
            self.tiempo_colision_tronco -= 1
            if self.tiempo_colision_tronco == 0:
                self.colision_tronco = False
                self.sprite_especial = False  # Volver al sprite normal

        # Acelerón con ESPACIO
        if keys[pygame.K_SPACE]:
            vel_actual = self.vel_aceleron

        # Efecto de turbulencia
        if self.dentro_turbulencia(tile_map):
            vel_actual = self.vel_turbulencia
            nuevo_x += random.choice([-1, 0, 1])
            nuevo_y += random.choice([-1, 0, 1])
            
            if not self.en_turbulencia:
                self.en_turbulencia = True
                self.mensaje_turbulencia = "Está pasando por un cúmulo de agua contaminada por mercurio y estás perdiendo vida"
            
            # Mantener mensaje mientras esté en turbulencia
            self.tiempo_mensaje = 60  # Renovar constantemente
            
            # Perder vida en turbulencia (más lento)
            self.vida -= 0.05
            if self.vida < 0:
                self.vida = 0
        else:
            if self.en_turbulencia:
                # Acaba de salir de turbulencia
                self.en_turbulencia = False
                self.tiempo_mensaje = 0  # Quitar mensaje inmediatamente
        
        # Actualizar mensaje
        if self.tiempo_mensaje > 0:
            self.tiempo_mensaje -= 1

        # Movimiento del barco
        if keys[pygame.K_LEFT]:
            nuevo_x -= vel_actual
            movio = True
        if keys[pygame.K_RIGHT]:
            nuevo_x += vel_actual
            movio = True
        if keys[pygame.K_UP]:
            nuevo_y -= vel_actual
            movio = True
        if keys[pygame.K_DOWN]:
            nuevo_y += vel_actual
            movio = True
        
        # Detectar movimiento para salir del estado de pesca
        if self.pescando and movio:
            self.pescando = False
        
        # Reset colision_tronco si se mueve y ya no está colisionando
        if self.colision_tronco:
            # Verificar si ya no está colisionando con ningún obstáculo
            colisionando = False
            if hasattr(tile_map, 'obstaculos_activos'):
                for obstaculo in tile_map.obstaculos_activos:
                    if obstaculo.collides_with_player(self.x, self.y):
                        colisionando = True
                        break
            if not colisionando:
                self.colision_tronco = False
                self.sprite_especial = False
                self.tiempo_colision_tronco = 0

        # Verificar si la nueva posición es válida
        temp_x, temp_y = self.x, self.y
        self.x, self.y = nuevo_x, nuevo_y
        
        # Verificar colisión con obstáculos dinámicos
        collision_with_obstacle = False
        if hasattr(tile_map, 'obstaculos_activos'):
            for obstaculo in tile_map.obstaculos_activos:
                if obstaculo.collides_with_player(self.x, self.y):
                    collision_with_obstacle = True
                    break
        
        # Verificar colisión con obstáculos estáticos
        if not collision_with_obstacle and hasattr(tile_map, 'obstacles'):
            for obstacle in tile_map.obstacles:
                if obstacle.collides_with_player(self.x, self.y):
                    collision_with_obstacle = True
                    break
        
        if self.en_agua(tile_map) and not collision_with_obstacle:
            pass  # Mantener nueva posición
        else:
            self.x, self.y = temp_x, temp_y  # Revertir

        # Animación
        if movio:
            self.contador_anim += 1
            if self.contador_anim % 10 == 0:
                self.frame = (self.frame + 1) % 2
    
    def buscar_pez_cercano(self, tile_map):
        """Busca un pez cerca del jugador"""
        if not hasattr(tile_map, 'peces_activos'):
            return None
            
        distancia_pesca = 50  # Distancia máxima para pescar
        
        for pez in tile_map.peces_activos:
            dx = pez.x - self.x
            dy = pez.y - self.y
            distancia = (dx * dx + dy * dy) ** 0.5
            
            if distancia <= distancia_pesca:
                return pez
        
        return None

def encontrar_posicion_inicial(tile_map):
    """Busca un punto válido en el agua"""
    while True:
        x = random.randint(200, MAP_ANCHO-200)
        y = random.randint(MAP_ALTO-800, MAP_ALTO-200)
        player = Player(x, y)
        if player.en_agua(tile_map):
            return x, y