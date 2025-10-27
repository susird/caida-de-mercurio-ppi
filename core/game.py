# core/game.py
import pygame
import random
from core.settings import MAP_ANCHO, MAP_ALTO, VERDE, SELVAS, AZUL1, AZUL2, TURBULENCIA

def generate_map():
    """Genera y devuelve (mapa, turbulencias)"""
    mapa = pygame.Surface((MAP_ANCHO, MAP_ALTO))
    mapa.fill(VERDE)

    # Selva: árboles pequeños
    for _ in range(5000):
        x = random.randint(0, MAP_ANCHO)
        y = random.randint(0, MAP_ALTO)
        radio = random.randint(5, 12)
        color_selva = random.choice(SELVAS)
        pygame.draw.circle(mapa, color_selva, (x, y), radio)

    turbulencias = []

    # Dibujar río principal y posibles turbulencias
    centro = MAP_ANCHO // 2
    ancho_rio = 300
    y = 0
    while y < MAP_ALTO:
        dx = random.choice([-150, -100, -50, 0, 50, 100, 150])
        centro = max(200, min(MAP_ANCHO - 200, centro + dx))
        color_agua = random.choice([AZUL1, AZUL2])

        pygame.draw.circle(mapa, color_agua, (centro, y), ancho_rio // 2)
        pygame.draw.circle(mapa, color_agua, (centro, y + 200), ancho_rio // 2)
        pygame.draw.rect(mapa, color_agua, (centro - ancho_rio // 2, y, ancho_rio, 200))

        # Turbulencias
        if random.random() < 0.25:
            t_x = centro + random.randint(-100, 100)
            t_y = y + random.randint(50, 250)
            radio = random.randint(60, 120)
            pygame.draw.circle(mapa, TURBULENCIA, (t_x, t_y), radio)
            turbulencias.append(pygame.Rect(t_x - radio, t_y - radio, radio * 2, radio * 2))

        y += 200

    return mapa, turbulencias

def run_game():
    """Función principal del juego"""
    import sys
    from core.settings import ANCHO, ALTO, FULLSCREEN
    from entities.player import Player, encontrar_posicion_inicial
    from utils.helpers import load_navegantes
    from ui.game_screen import GameScreen

    pygame.init()
    if FULLSCREEN:
        screen = pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Río con Selva y Turbulencias")
    clock = pygame.time.Clock()

    # Generar mapa y turbulencias
    mapa, turbulencias = generate_map()

    # Cargar imágenes
    imagenes_navegante, navegante_rio1 = load_navegantes()

    # Crear jugador
    barco_x, barco_y = encontrar_posicion_inicial(mapa)
    player = Player(barco_x, barco_y)

    # Crear pantalla de juego
    game_screen = GameScreen()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                accion = game_screen.handle_click(event.pos)
                if accion == "volver":
                    running = False

        # Actualizar jugador
        keys = pygame.key.get_pressed()
        player.update(keys, mapa, turbulencias)

        # Actualizar cámara
        game_screen.update_camera(player.x, player.y)

        # Dibujar
        game_screen.draw(screen, mapa, player, imagenes_navegante, navegante_rio1)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()