import pygame
import random
from core.settings import MAP_ANCHO, MAP_ALTO, ANCHO, ALTO, FULLSCREEN
from entities.fish import Fish
from entities.obstaculo import Obstaculo
from entities.player import Player, encontrar_posicion_inicial
from core.tile_map import TileMap
from utils.helpers import load_navegantes
from ui.game_screen import GameScreen
from ui.game_over_screen import GameOverScreen
from ui.win_screen import WinScreen
from config.game_config import DIFFICULTY_SETTINGS
from data.game_data import GameData
from data.save_game import SaveGame

class GameManager:
    DIFFICULTY_SEEDS = {"novato": 12345, "medio": 67890, "pro": 54321}
    
    def __init__(self, difficulty="novato", saved_data=None):
        self.difficulty = difficulty
        self.saved_data = saved_data
        self.difficulty_config = DIFFICULTY_SETTINGS[difficulty]
        
        if not pygame.get_init():
            pygame.init()
            
        self.screen = self._init_screen()
        self.clock = pygame.time.Clock()
        
        self.tile_map = None
        self.player = None
        self.fish_list = []
        self.obstacles_list = []
        
        self.game_screen = GameScreen()
        self.game_over_screen = GameOverScreen()
        self.win_screen = WinScreen()
        
        self.game_over = False
        self.victory = False
        self.game_over_reason = "death"
        
        self.game_data = GameData()
        self.save_game = SaveGame()
        self.obstacles_hit = 0
        self.data_saved = False
    
    def _init_screen(self):
        if FULLSCREEN:
            return pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN)
        return pygame.display.set_mode((ANCHO, ALTO))
    
    def generate_world(self):
        seed = self.DIFFICULTY_SEEDS.get(self.difficulty, 12345)
        random.seed(seed)
        
        self.tile_map = TileMap(seed)
        self._generate_fish()
        self._generate_obstacles()
        
        import time
        random.seed(int(time.time()))
        
        self.tile_map.peces_activos = self.fish_list
        self.tile_map.obstaculos_activos = self.obstacles_list
        
        self.original_fish_positions = {(int(fish.x), int(fish.y)) for fish in self.fish_list}
        self.original_fish_count = len(self.fish_list)
        
        if self.saved_data:
            saved_x, saved_y = self.saved_data["player_x"], self.saved_data["player_y"]
            
            if self._is_valid_water_position(saved_x, saved_y):
                self.player = Player(saved_x, saved_y)
            else:
                boat_x, boat_y = self._find_nearby_water_position(saved_x, saved_y)
                self.player = Player(boat_x, boat_y)
            
            self.player.health = self.saved_data["health"]
            self.player.fish_collected = self.saved_data["fish_collected"]
            elapsed_ms = self.saved_data["elapsed_time"] * 1000
            self.player.start_time = pygame.time.get_ticks() - elapsed_ms
            
            self._restore_fished_state()
        else:
            boat_x, boat_y = encontrar_posicion_inicial(self.tile_map)
            self.player = Player(boat_x, boat_y)
        

    
    def _generate_fish(self):
        self.fish_list = []
        for _ in range(1500):
            x = random.randint(100, MAP_ANCHO - 100)
            y = random.randint(100, MAP_ALTO - 100)
            
            tile_type = self.tile_map.get_tile_at_pixel(x, y)
            if self.tile_map.is_water_tile(tile_type):
                fish_type = self._determine_fish_type(tile_type)
                self.fish_list.append(Fish(x, y, fish_type))
                
                if len(self.fish_list) >= 200:
                    break
    
    def _determine_fish_type(self, tile_type):
        if self.tile_map.is_turbulence_tile(tile_type):
            rand = random.random()
            if rand < 0.7:
                return "good"
            elif rand < 0.85:
                return "normal"
            else:
                return "high_mercury"
        else:
            rand = random.random()
            if rand < 0.15:
                return "good"
            elif rand < 0.65:
                return "normal"
            else:
                return "high_mercury"
    
    def _generate_obstacles(self):
        self.obstacles_list = []
        for _ in range(1000):
            x = random.randint(200, MAP_ANCHO - 200)
            y = random.randint(200, MAP_ALTO - 200)
            
            tile_type = self.tile_map.get_tile_at_pixel(x, y)
            if self.tile_map.is_water_tile(tile_type):
                obstacle_type = "tronco" if random.random() < 0.8 else "barril"
                self.obstacles_list.append(Obstaculo(x, y, obstacle_type))
                
                if len(self.obstacles_list) >= 100:
                    break
    
    def update_game_state(self):
        if self.player.health <= 0 and not self.game_over:
            self.game_over = True
            self.game_over_reason = "death"
        elif self.player.fish_collected >= self.difficulty_config["fish_goal"] and not self.victory:
            self.victory = True
        
        elapsed_time = (pygame.time.get_ticks() - self.player.start_time) / 1000
        if elapsed_time >= self.difficulty_config["time_limit"] and not self.game_over and not self.victory:
            self.game_over = True
            self.game_over_reason = "timeout"
    
    def update_entities(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.tile_map)
        
        for fish in self.fish_list:
            fish.update(self.tile_map)
        
        for obstacle in self.obstacles_list:
            obstacle.update(self.tile_map, self.player.y, self.player.fish_collected)
        
        self._spawn_new_obstacles()
        self.tile_map.update_jungle()
    
    def _spawn_new_obstacles(self):
        progress = self.player.y / MAP_ALTO
        spawn_chance = 0.002 + (progress * 0.008)
        
        if random.random() < spawn_chance:
            for _ in range(20):
                x = random.randint(100, MAP_ANCHO - 100)
                y = self.player.y - random.randint(200, 500)
                
                if self.tile_map.is_water_tile(self.tile_map.get_tile_at_pixel(x, y)):
                    obstacle_type = "tronco" if random.random() < 0.8 else "barril"
                    new_obstacle = Obstaculo(x, y, obstacle_type)
                    self.obstacles_list.append(new_obstacle)
                    self.tile_map.obstaculos_activos.append(new_obstacle)
                    break
    
    def handle_events(self):
        events = pygame.event.get()
        
        # Si está en game over o victoria, solo manejar esos eventos
        if self.game_over:
            action = self.game_over_screen.handle_events(events)
            if action:
                return action
        elif self.victory:
            for event in events:
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "menu"
        else:
            # Eventos normales del juego
            for event in events:
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    action = self.game_screen.handle_click(event.pos)
                    if action == "volver":
                        return "menu"
                    elif action == "salir":
                        return "quit"
        
        return None
    
    def render(self):
        if self.victory:
            self.win_screen.draw(self.screen)
        elif self.game_over:
            self.game_over_screen.draw(self.screen, self.game_over_reason)
        else:
            self.game_screen.update_camera(self.player.x, self.player.y)
            
            try:
                navegantes, navegante_rio1, navegante_especial, navegante_pescando = load_navegantes()
                
                self.game_screen.draw(
                    self.screen, self.tile_map, self.player, navegantes,
                    navegante_rio1, self.fish_list, navegante_especial,
                    navegante_pescando, self.obstacles_list, self.difficulty_config["time_limit"]
                )
            except Exception as e:
                print(f"Error en render: {e}")
                return "menu"
        
        pygame.display.flip()
    
    def run(self):
        pygame.display.set_caption("Río con Selva y Turbulencias")
        self.generate_world()
        
        running = True
        while running:
            action = self.handle_events()
            if action:
                if action == "menu" and not (self.game_over or self.victory) and self.player.fish_collected > 0:
                    elapsed_time = (pygame.time.get_ticks() - self.player.start_time) / 1000
                    fished_positions = []
                    if hasattr(self, 'original_fish_count'):
                        current_positions = {(int(fish.x), int(fish.y)) for fish in self.fish_list}
                        original_positions = getattr(self, 'original_fish_positions', set())
                        fished_positions = list(original_positions - current_positions)
                    
                    self.save_game.save_current_game(self.difficulty, self.player, elapsed_time, fished_positions)
                elif (self.game_over or self.victory):
                    self.save_game.delete_saved_game(self.difficulty)
                return action
            
            if not (self.game_over or self.victory):
                self.update_entities()
            
            self.update_game_state()
            
            if (self.game_over or self.victory) and not self.data_saved:
                self._save_game_data()
            
            self.render()
            self.clock.tick(60)
        
        return "menu"

    def _save_game_data(self):
        if self.data_saved:
            return
        
        try:
            elapsed_time = (pygame.time.get_ticks() - self.player.start_time) / 1000
            
            self.game_data.save_score(self.difficulty, self.player.fish_collected, elapsed_time, self.victory)
            self.game_data.update_progress(self.difficulty, elapsed_time, self.victory)
            self.game_data.update_stats(self.player.fish_collected, self.obstacles_hit, elapsed_time, self.victory)
        except Exception as e:
            print(f"Error guardando datos: {e}")
        
        self.data_saved = True
    
    def _is_valid_water_position(self, x, y):
        if not (0 <= x < MAP_ANCHO and 0 <= y < MAP_ALTO):
            return False
        return self.tile_map.is_water_tile(self.tile_map.get_tile_at_pixel(x, y))
    
    def _find_nearby_water_position(self, target_x, target_y):
        import math
        for radius in range(50, 500, 50):
            for angle in range(0, 360, 30):
                x = target_x + radius * math.cos(math.radians(angle))
                y = target_y + radius * math.sin(math.radians(angle))
                
                if self._is_valid_water_position(x, y):
                    return x, y
        
        return encontrar_posicion_inicial(self.tile_map)
    
    def _generate_additional_fish(self, count):
        """Genera peces adicionales cuando hay muy pocos"""
        for _ in range(count * 3):  # Más intentos
            x = random.randint(100, MAP_ANCHO - 100)
            y = random.randint(100, MAP_ALTO - 100)
            
            tile_type = self.tile_map.get_tile_at_pixel(x, y)
            if self.tile_map.is_water_tile(tile_type):
                fish_type = self._determine_fish_type(tile_type)
                self.fish_list.append(Fish(x, y, fish_type))
                
                if len(self.fish_list) >= count + 50:
                    break
    
    def _restore_fished_state(self):
        if "fished_positions" in self.saved_data and self.saved_data["fished_positions"]:
            fished_positions = set()
            for pos in self.saved_data["fished_positions"]:
                if isinstance(pos, (list, tuple)) and len(pos) >= 2:
                    fished_positions.add((int(pos[0]), int(pos[1])))
            
            # Remover peces que ya fueron pescados
            remaining_fish = []
            for fish in self.fish_list:
                fish_pos = (int(fish.x), int(fish.y))
                if fish_pos not in fished_positions:
                    remaining_fish.append(fish)
            
            self.fish_list = remaining_fish
            
            # Si quedan muy pocos peces, generar más
            if len(self.fish_list) < 50:
                self._generate_additional_fish(150 - len(self.fish_list))
            
            self.tile_map.peces_activos = self.fish_list
            print(f"Restaurado: {len(self.fish_list)} peces restantes de {self.original_fish_count} originales")

def run_game_window(difficulty="novato", saved_data=None):
    game_manager = GameManager(difficulty, saved_data)
    return game_manager.run()