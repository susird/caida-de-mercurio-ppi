# core/game.py
import pygame
import random
from core.settings import MAP_ANCHO, MAP_ALTO, VERDE, SELVAS, AZUL1, AZUL2, TURBULENCIA
from entities.fish import Fish
from entities.obstaculo import Obstaculo
from core.tile_map import TileMap

def generate_map():
    """Genera y devuelve (tile_map, peces, troncos)"""
    tile_map = TileMap()
    
    # Generar más peces para el mapa más grande
    peces = []
    for _ in range(1500):  # Más peces
        x = random.randint(100, MAP_ANCHO - 100)
        y = random.randint(100, MAP_ALTO - 100)
        
        tile_type = tile_map.get_tile_at_pixel(x, y)
        if tile_map.is_water_tile(tile_type):
            if tile_map.is_turbulence_tile(tile_type):
                # En turbulencias: 60% buenos, 25% normales, 15% muy contaminados
                rand = random.random()
                if rand < 0.6:
                    fish_type = "good"
                elif rand < 0.85:
                    fish_type = "normal"
                else:
                    fish_type = "high_mercury"
            else:
                # En agua normal: solo normales y muy contaminados (NO peces buenos)
                rand = random.random()
                if rand < 0.6:
                    fish_type = "normal"
                else:
                    fish_type = "high_mercury"
            
            peces.append(Fish(x, y, fish_type))
            if len(peces) >= 200:  # Más peces totales
                break
    
    # Generar más obstáculos para el mapa más grande
    obstaculos = []
    for _ in range(1000):  # Más intentos
        x = random.randint(200, MAP_ANCHO - 200)
        y = random.randint(200, MAP_ALTO - 200)
        
        tile_type = tile_map.get_tile_at_pixel(x, y)
        if tile_map.is_water_tile(tile_type):
            tipo = random.choice(["tronco", "barril"])
            obstaculos.append(Obstaculo(x, y, tipo))
            if len(obstaculos) >= 100:  # Muchos más obstáculos
                break

    return tile_map, peces, obstaculos

def run_game():
    return run_game_window()

def run_game_window(dificultad="novato"):
    from core.settings import ANCHO, ALTO, FULLSCREEN
    from entities.player import Player, encontrar_posicion_inicial
    from utils.helpers import load_navegantes
    from ui.game_screen import GameScreen
    from ui.game_over_screen import GameOverScreen
    from ui.win_screen import WinScreen

    if FULLSCREEN:
        screen = pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Río con Selva y Turbulencias")
    clock = pygame.time.Clock()

    # Generar mapa, peces y obstáculos
    tile_map, peces, obstaculos = generate_map()
    # Agregar peces y obstáculos al tile_map para que el player pueda acceder
    tile_map.peces_activos = peces
    tile_map.obstaculos_activos = obstaculos
    
    print(f"Generados {len(obstaculos)} obstáculos")  # Debug

    # Cargar imágenes
    imagenes_navegante, navegante_rio1, navegante_especial, navegante_pescando = load_navegantes()

    # Crear jugador
    barco_x, barco_y = encontrar_posicion_inicial(tile_map)
    player = Player(barco_x, barco_y)
    player.dificultad = dificultad

    # Crear pantallas
    game_screen = GameScreen()
    game_over_screen = GameOverScreen()
    win_screen = WinScreen()
    game_over = False
    victoria = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                accion = game_screen.handle_click(event.pos)
                if accion == "volver":
                    return "menu"
                elif accion == "salir":
                    return "quit"

        # Verificar Game Over o Victoria
        if player.vida <= 0 and not game_over:
            game_over = True
        elif player.peces_recolectados >= 20 and not victoria:
            victoria = True
        
        # Verificar tiempo límite según dificultad
        tiempo_transcurrido = (pygame.time.get_ticks() - player.tiempo_inicio) / 1000
        tiempo_limite = {"novato": 180, "medio": 120, "pro": 60}[dificultad]
        if tiempo_transcurrido >= tiempo_limite and not game_over and not victoria:
            game_over = True
        
        if victoria:
            # Pantalla de Victoria
            win_screen.draw(screen)
            
            # Manejar eventos de Victoria
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"
        elif game_over:
            # Pantalla de Game Over
            game_over_screen.draw(screen)
            
            # Manejar eventos de Game Over
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"
        else:
            # Juego normal
            # Actualizar jugador
            keys = pygame.key.get_pressed()
            player.update(keys, tile_map)
            
            # Actualizar peces
            for pez in peces:
                pez.update(tile_map)
            
            # Actualizar obstáculos con velocidad progresiva
            for obstaculo in obstaculos:
                obstaculo.update(tile_map, player.y)
            
            # Generar más obstáculos según progreso
            from core.settings import MAP_ALTO
            progreso = player.y / MAP_ALTO
            if random.random() < 0.002 + (progreso * 0.008):  # Más frecuencia
                # Buscar posición en agua cerca del jugador
                for _ in range(20):
                    x = random.randint(100, MAP_ANCHO - 100)
                    y = player.y - random.randint(200, 500)  # Aparecer arriba del jugador
                    if tile_map.is_water_tile(tile_map.get_tile_at_pixel(x, y)):
                        tipo = random.choice(["tronco", "barril"])
                        nuevo_obstaculo = Obstaculo(x, y, tipo)
                        obstaculos.append(nuevo_obstaculo)
                        tile_map.obstaculos_activos.append(nuevo_obstaculo)
                        break
            
            # Actualizar selva
            tile_map.update_jungle()

            # Actualizar cámara
            game_screen.update_camera(player.x, player.y)

            # Dibujar
            game_screen.draw(screen, tile_map, player, imagenes_navegante, navegante_rio1, peces, navegante_especial, navegante_pescando, obstaculos)

        pygame.display.flip()
        clock.tick(60)

    return "menu"