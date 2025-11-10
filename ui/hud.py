# ui/hud.py
import os
import pygame
from core.settings import FONTS_DIR
from utils.constants import CREMA, NEGRO

class HUD:
    def __init__(self):
        font_path = os.path.join(FONTS_DIR, "VT323-Regular.ttf")
        self.fuente = pygame.font.Font(font_path, 24)

    def draw_vida(self, surface, vida):
        """Dibuja la barra de vida"""
        # Texto de vida
        vida_texto = f"VIDA: {int(vida)}"
        vida_surface = self.fuente.render(vida_texto, True, CREMA)
        surface.blit(vida_surface, (20, 20))
        
        # Barra de vida visual
        barra_ancho = 200
        barra_alto = 20
        vida_porcentaje = vida / 100
        
        # Fondo de la barra
        pygame.draw.rect(surface, NEGRO, (20, 50, barra_ancho, barra_alto))
        # Vida actual
        color_vida = (255, 0, 0) if vida < 30 else (255, 255, 0) if vida < 60 else (0, 255, 0)
        pygame.draw.rect(surface, color_vida, (20, 50, int(barra_ancho * vida_porcentaje), barra_alto))

    def draw_mensaje(self, surface, mensaje, tiempo_restante, player_x, player_y, cam_x, cam_y):
        """Dibuja cuadro de diálogo rojo para turbulencias"""
        if tiempo_restante > 0:
            # Posición del jugador en pantalla
            screen_x = int(player_x - cam_x)
            screen_y = int(player_y - cam_y)
            
            # Renderizar texto en negro
            mensaje_surface = self.fuente.render(mensaje, True, (0, 0, 0))
            
            # Tamaño del cuadro de diálogo
            padding = 10
            cuadro_ancho = mensaje_surface.get_width() + padding * 2
            cuadro_alto = mensaje_surface.get_height() + padding * 2
            
            # Posición del cuadro (arriba del jugador)
            cuadro_x = screen_x - cuadro_ancho // 2
            cuadro_y = screen_y - 120  # Más arriba para no chocar con el de peces
            
            # Ajustar si se sale de la pantalla
            cuadro_x = max(10, min(surface.get_width() - cuadro_ancho - 10, cuadro_x))
            cuadro_y = max(10, cuadro_y)
            
            # Dibujar fondo rojo con borde negro
            pygame.draw.rect(surface, (255, 100, 100), (cuadro_x, cuadro_y, cuadro_ancho, cuadro_alto))
            pygame.draw.rect(surface, (0, 0, 0), (cuadro_x, cuadro_y, cuadro_ancho, cuadro_alto), 2)
            
            # Dibujar texto
            texto_x = cuadro_x + padding
            texto_y = cuadro_y + padding
            surface.blit(mensaje_surface, (texto_x, texto_y))
            
            # Dibujar puntita del cuadro hacia el jugador
            punta_x = screen_x
            punta_y = cuadro_y + cuadro_alto
            pygame.draw.polygon(surface, (255, 100, 100), [
                (punta_x - 8, punta_y),
                (punta_x + 8, punta_y),
                (punta_x, punta_y + 10)
            ])
            pygame.draw.polygon(surface, (0, 0, 0), [
                (punta_x - 8, punta_y),
                (punta_x + 8, punta_y),
                (punta_x, punta_y + 10)
            ], 2)
    
    def draw_mensaje_pez(self, surface, mensaje, player_x, player_y, cam_x, cam_y):
        """Dibuja cuadro de diálogo junto al jugador"""
        # Posición del jugador en pantalla
        screen_x = int(player_x - cam_x)
        screen_y = int(player_y - cam_y)
        
        # Color del cuadro según el mensaje
        if "Recuperas" in mensaje:
            fondo_color = (100, 255, 100)  # Verde para peces buenos
        elif "muy contaminado" in mensaje:
            fondo_color = (255, 50, 50)    # Rojo oscuro para muy tóxicos
        else:
            fondo_color = (255, 255, 255)  # Blanco para normales
        
        # Renderizar texto
        mensaje_surface = self.fuente.render(mensaje, True, (0, 0, 0))  # Texto negro
        
        # Tamaño del cuadro de diálogo
        padding = 10
        cuadro_ancho = mensaje_surface.get_width() + padding * 2
        cuadro_alto = mensaje_surface.get_height() + padding * 2
        
        # Posición del cuadro (arriba del jugador)
        cuadro_x = screen_x - cuadro_ancho // 2
        cuadro_y = screen_y - 80  # 80 píxeles arriba del jugador
        
        # Ajustar si se sale de la pantalla
        cuadro_x = max(10, min(surface.get_width() - cuadro_ancho - 10, cuadro_x))
        cuadro_y = max(10, cuadro_y)
        
        # Dibujar fondo con color según tipo de pez
        pygame.draw.rect(surface, fondo_color, (cuadro_x, cuadro_y, cuadro_ancho, cuadro_alto))
        pygame.draw.rect(surface, (0, 0, 0), (cuadro_x, cuadro_y, cuadro_ancho, cuadro_alto), 2)
        
        # Dibujar texto
        texto_x = cuadro_x + padding
        texto_y = cuadro_y + padding
        surface.blit(mensaje_surface, (texto_x, texto_y))
        
        # Dibujar puntita del cuadro hacia el jugador
        punta_x = screen_x
        punta_y = cuadro_y + cuadro_alto
        pygame.draw.polygon(surface, fondo_color, [
            (punta_x - 8, punta_y),
            (punta_x + 8, punta_y),
            (punta_x, punta_y + 10)
        ])
        pygame.draw.polygon(surface, (0, 0, 0), [
            (punta_x - 8, punta_y),
            (punta_x + 8, punta_y),
            (punta_x, punta_y + 10)
        ], 2)
    
    def draw_contador_peces(self, surface, peces_recolectados):
        """Dibuja el contador de peces recolectados"""
        # Texto del contador
        contador_texto = f"PECES: {peces_recolectados}/20"
        contador_surface = self.fuente.render(contador_texto, True, CREMA)
        surface.blit(contador_surface, (20, 80))
        
        # Barra visual de progreso
        barra_ancho = 200
        barra_alto = 15
        progreso = min(peces_recolectados / 20, 1.0)
        
        # Fondo de la barra
        pygame.draw.rect(surface, NEGRO, (20, 105, barra_ancho, barra_alto))
        # Progreso actual
        color_progreso = (0, 255, 0) if peces_recolectados >= 20 else (255, 215, 0)
        pygame.draw.rect(surface, color_progreso, (20, 105, int(barra_ancho * progreso), barra_alto))
    
    def draw_tiempo(self, surface, tiempo_inicio, dificultad="novato"):
        """Dibuja el temporizador"""
        tiempo_transcurrido = (pygame.time.get_ticks() - tiempo_inicio) / 1000
        tiempo_limite = {"novato": 180, "medio": 120, "pro": 60}[dificultad]
        tiempo_restante = max(0, tiempo_limite - tiempo_transcurrido)
        
        minutos = int(tiempo_restante // 60)
        segundos = int(tiempo_restante % 60)
        
        tiempo_texto = f"TIEMPO: {minutos:02d}:{segundos:02d}"
        tiempo_surface = self.fuente.render(tiempo_texto, True, CREMA)
        surface.blit(tiempo_surface, (20, 130))
    
    def draw_mensaje_tronco(self, surface, mensaje, player_x, player_y, cam_x, cam_y):
        """Dibuja cuadro de diálogo para colisión con tronco"""
        # Posición del jugador en pantalla
        screen_x = int(player_x - cam_x)
        screen_y = int(player_y - cam_y)
        
        # Color naranja para troncos
        fondo_color = (255, 165, 0)
        
        # Renderizar texto
        mensaje_surface = self.fuente.render(mensaje, True, (0, 0, 0))  # Texto negro
        
        # Tamaño del cuadro de diálogo
        padding = 10
        cuadro_ancho = mensaje_surface.get_width() + padding * 2
        cuadro_alto = mensaje_surface.get_height() + padding * 2
        
        # Posición del cuadro (arriba del jugador, diferente altura que otros mensajes)
        cuadro_x = screen_x - cuadro_ancho // 2
        cuadro_y = screen_y - 160  # Más arriba para no chocar con otros mensajes
        
        # Ajustar si se sale de la pantalla
        cuadro_x = max(10, min(surface.get_width() - cuadro_ancho - 10, cuadro_x))
        cuadro_y = max(10, cuadro_y)
        
        # Dibujar fondo naranja
        pygame.draw.rect(surface, fondo_color, (cuadro_x, cuadro_y, cuadro_ancho, cuadro_alto))
        pygame.draw.rect(surface, (0, 0, 0), (cuadro_x, cuadro_y, cuadro_ancho, cuadro_alto), 2)
        
        # Dibujar texto
        texto_x = cuadro_x + padding
        texto_y = cuadro_y + padding
        surface.blit(mensaje_surface, (texto_x, texto_y))
        
        # Dibujar puntita del cuadro hacia el jugador
        punta_x = screen_x
        punta_y = cuadro_y + cuadro_alto
        pygame.draw.polygon(surface, fondo_color, [
            (punta_x - 8, punta_y),
            (punta_x + 8, punta_y),
            (punta_x, punta_y + 10)
        ])
        pygame.draw.polygon(surface, (0, 0, 0), [
            (punta_x - 8, punta_y),
            (punta_x + 8, punta_y),
            (punta_x, punta_y + 10)
        ], 2)