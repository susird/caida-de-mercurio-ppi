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

    def en_agua(self, mapa):
        """Verifica si el centro del barco está en agua"""
        if 0 <= self.x < MAP_ANCHO and 0 <= self.y < MAP_ALTO:
            color = mapa.get_at((int(self.x), int(self.y)))
            return color[:3] in (AZUL1, AZUL2, TURBULENCIA)
        return False

    def dentro_turbulencia(self, turbulencias):
        """Detecta si el barco está en una zona de turbulencia"""
        barco_rect = pygame.Rect(int(self.x-25), int(self.y-15), 50, 30)
        for t in turbulencias:
            if barco_rect.colliderect(t):
                return True
        return False

    def update(self, keys, mapa, turbulencias):
        """Actualiza la posición del jugador"""
        vel_actual = self.vel
        nuevo_x, nuevo_y = self.x, self.y

        # Acelerón con ESPACIO
        if keys[pygame.K_SPACE]:
            vel_actual = self.vel_aceleron

        # Efecto de turbulencia
        if self.dentro_turbulencia(turbulencias):
            vel_actual = self.vel_turbulencia
            nuevo_x += random.choice([-1, 0, 1])
            nuevo_y += random.choice([-1, 0, 1])
            
            if not self.en_turbulencia:
                self.en_turbulencia = True
                self.mensaje_turbulencia = "¡TURBULENCIA! Navegación lenta - Perdiendo vida"
                self.tiempo_mensaje = 180  # 3 segundos a 60 FPS
            
            # Perder vida en turbulencia (más lento)
            self.vida -= 0.05
            if self.vida < 0:
                self.vida = 0
        else:
            self.en_turbulencia = False
        
        # Actualizar mensaje
        if self.tiempo_mensaje > 0:
            self.tiempo_mensaje -= 1

        # Movimiento del barco
        movio = False
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

        # Verificar si la nueva posición es válida
        temp_x, temp_y = self.x, self.y
        self.x, self.y = nuevo_x, nuevo_y
        if self.en_agua(mapa):
            pass  # Mantener nueva posición
        else:
            self.x, self.y = temp_x, temp_y  # Revertir

        # Animación
        if movio:
            self.contador_anim += 1
            if self.contador_anim % 10 == 0:
                self.frame = (self.frame + 1) % 2

def encontrar_posicion_inicial(mapa):
    """Busca un punto válido en el agua"""
    while True:
        x = random.randint(200, MAP_ANCHO-200)
        y = random.randint(MAP_ALTO-800, MAP_ALTO-200)
        player = Player(x, y)
        if player.en_agua(mapa):
            return x, y