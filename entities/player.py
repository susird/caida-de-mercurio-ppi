import random
import pygame
from core.settings import MAP_ANCHO, MAP_ALTO
from config.settings import SOUNDS_DIR
from utils.constants import BARCO_VEL, BARCO_VEL_TURBULENCIA, BARCO_VEL_ACELERON

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 100
        self.fish_collected = 0
        self.start_time = pygame.time.get_ticks()
        
        self._init_movement()
        self._init_animation()
        self._init_states()
        self._init_messages()
        # Cargar sonido de colisión si está disponible
        self.collision_sound = None
        try:
            if pygame.mixer.get_init():
                sound_file = SOUNDS_DIR / "explosion.mp3"
                if sound_file.exists():
                    self.collision_sound = pygame.mixer.Sound(str(sound_file))
                    try:
                        self.collision_sound.set_volume(0.7)
                    except Exception:
                        pass
        except Exception:
            # No es crítico si falla la carga del sonido
            self.collision_sound = None

        # Cargar sonido de latido (salud baja) si está disponible
        self.heartbeat_sound = None
        self.heartbeat_playing = False
        try:
            if pygame.mixer.get_init():
                hb_file = SOUNDS_DIR / "HeartBeat.mp3"
                if hb_file.exists():
                    self.heartbeat_sound = pygame.mixer.Sound(str(hb_file))
                    try:
                        self.heartbeat_sound.set_volume(0.6)
                    except Exception:
                        pass
        except Exception:
            self.heartbeat_sound = None
    
    def _init_movement(self):
        self.normal_speed = BARCO_VEL
        self.turbulence_speed = BARCO_VEL_TURBULENCIA
        self.boost_speed = BARCO_VEL_ACELERON
    
    def _init_animation(self):
        self.frame = 0
        self.animation_counter = 0
    
    def _init_states(self):
        self.in_turbulence = False
        self.is_fishing = False
        self.has_collision = False
        self.show_special_sprite = False
    
    def _init_messages(self):
        self.turbulence_message = ""
        self.turbulence_message_timer = 0
        self.fish_message = ""
        self.fish_message_timer = 0
        self.collision_message = ""
        self.collision_message_timer = 0

    def is_in_water(self, tile_map):
        if not (0 <= self.x < MAP_ANCHO and 0 <= self.y < MAP_ALTO):
            return False
        tile_type = tile_map.get_tile_at_pixel(self.x, self.y)
        return tile_map.is_water_tile(tile_type)

    def is_in_turbulence(self, tile_map):
        tile_type = tile_map.get_tile_at_pixel(self.x, self.y)
        return tile_map.is_turbulence_tile(tile_type)

    def _handle_fishing(self, keys, tile_map):
        if keys[pygame.K_s] and not self.is_fishing and self.fish_message_timer == 0:
            nearby_fish = self._find_nearby_fish(tile_map)
            if nearby_fish:
                self._catch_fish(nearby_fish, tile_map)

    def _find_nearby_fish(self, tile_map):
        if not hasattr(tile_map, 'peces_activos'):
            return None
            
        fishing_distance = 50
        
        for fish in tile_map.peces_activos:
            dx = fish.x - self.x
            dy = fish.y - self.y
            distance = (dx * dx + dy * dy) ** 0.5
            
            if distance <= fishing_distance:
                return fish
        
        return None

    def _catch_fish(self, fish, tile_map):
        if hasattr(tile_map, 'peces_activos'):
            tile_map.peces_activos.remove(fish)
        
        self.is_fishing = True
        damage = fish.mercury_damage
        fish_name = fish.fish_name
        
        # Reproducir sonido de pescar
        from utils.sound_manager import sound_manager
        sound_manager.play_fishing()
        
        if damage > 0:
            self.health = max(0, self.health - damage)
            self.fish_collected += 1
            self.fish_message = f"{fish_name} - Pierdes {damage} puntos"
        else:
            self.health = min(100, self.health + abs(damage))
            self.fish_collected += 2
            self.fish_message = f"{fish_name} - Ganas {abs(damage)} puntos"
        
        self.fish_message_timer = 10

    def _handle_obstacle_collision(self, tile_map):
        if not hasattr(tile_map, 'obstaculos_activos'):
            return
            
        for obstacle in tile_map.obstaculos_activos:
            if obstacle.collides_with_player(self.x, self.y) and not self.has_collision:
                damage = 2 if self.is_in_turbulence(tile_map) else 1
                message = "¡Agua tóxica! Pierdes 2 puntos de vida" if damage == 2 else "¡Plaf! Pierdes 1 punto de vida"
                
                self.health = max(0, self.health - damage)
                self.collision_message = message
                self.collision_message_timer = 180
                self.has_collision = True
                self.show_special_sprite = True
                # Reproducir el sonido existente de colisión
                try:
                    if self.collision_sound:
                        self.collision_sound.play()
                except Exception:
                    pass
                break

    def _handle_turbulence_effects(self, tile_map, new_x, new_y, current_speed):
        if self.is_in_turbulence(tile_map):
            current_speed = self.turbulence_speed
            new_x += random.choice([-1, 0, 1])
            new_y += random.choice([-1, 0, 1])
            
            if not self.in_turbulence:
                self.in_turbulence = True
                self.turbulence_message = "Está pasando por un cúmulo de agua contaminada por mercurio y estás perdiendo vida"
            
            self.turbulence_message_timer = 60
            self.health -= 0.05
            if self.health < 0:
                self.health = 0
        else:
            if self.in_turbulence:
                self.in_turbulence = False
                self.turbulence_message_timer = 0
        
        return new_x, new_y, current_speed

    def _handle_movement(self, keys, current_speed, new_x, new_y):
        has_moved = False
        
        if keys[pygame.K_LEFT]:
            new_x -= current_speed
            has_moved = True
        if keys[pygame.K_RIGHT]:
            new_x += current_speed
            has_moved = True
        if keys[pygame.K_UP]:
            new_y -= current_speed
            has_moved = True
        if keys[pygame.K_DOWN]:
            new_y += current_speed
            has_moved = True
        
        return new_x, new_y, has_moved

    def _reset_collision_state(self, tile_map):
        if not self.has_collision:
            return
            
        is_colliding = False
        if hasattr(tile_map, 'obstaculos_activos'):
            for obstacle in tile_map.obstaculos_activos:
                if obstacle.collides_with_player(self.x, self.y):
                    is_colliding = True
                    break
        
        if not is_colliding:
            self.has_collision = False
            self.show_special_sprite = False
            self.collision_message_timer = 0

    def _validate_and_apply_position(self, new_x, new_y, tile_map):
        temp_x, temp_y = self.x, self.y
        self.x, self.y = new_x, new_y
        
        collision_with_obstacle = self._check_obstacle_collision(tile_map)
        
        if self.is_in_water(tile_map) and not collision_with_obstacle:
            pass
        else:
            self.x, self.y = temp_x, temp_y

    def _check_obstacle_collision(self, tile_map):
        if hasattr(tile_map, 'obstaculos_activos'):
            for obstacle in tile_map.obstaculos_activos:
                if obstacle.collides_with_player(self.x, self.y):
                    return True
        
        if hasattr(tile_map, 'obstacles'):
            for obstacle in tile_map.obstacles:
                if obstacle.collides_with_player(self.x, self.y):
                    return True
        
        return False

    def _update_messages(self):
        if self.fish_message_timer > 0:
            self.fish_message_timer -= 1
        
        if self.collision_message_timer > 0:
            self.collision_message_timer -= 1
            if self.collision_message_timer == 0:
                self.has_collision = False
                self.show_special_sprite = False
        
        if self.turbulence_message_timer > 0:
            self.turbulence_message_timer -= 1

    def _update_animation(self, has_moved):
        if has_moved:
            self.animation_counter += 1
            if self.animation_counter % 10 == 0:
                self.frame = (self.frame + 1) % 2
    
    def _handle_low_health_sound(self):
        """
        Reproduce un sonido de latido en loop cuando la vida llega a 20 o menos y
        lo detiene cuando sube por encima de 20.
        """
        try:
            if not self.heartbeat_sound:
                return

            if self.health <= 20 and not self.heartbeat_playing:
                self.heartbeat_sound.play(-1)  # loop infinito hasta que se detenga
                self.heartbeat_playing = True
            elif self.health > 20 and self.heartbeat_playing:
                self.heartbeat_sound.stop()
                self.heartbeat_playing = False
        except Exception:
            # No detener la ejecución del juego por fallos en audio
            pass

    def update(self, keys, tile_map):
        current_speed = self.normal_speed
        new_x, new_y = self.x, self.y
        
        self._handle_fishing(keys, tile_map)
        self._update_messages()
        self._handle_obstacle_collision(tile_map)
        
        # Aplicar efectos de turbulencia primero
        new_x, new_y, current_speed = self._handle_turbulence_effects(tile_map, new_x, new_y, current_speed)
        
        # Luego aplicar turbo si se presiona espacio
        if keys[pygame.K_SPACE]:
            current_speed = self.boost_speed        
        new_x, new_y, has_moved = self._handle_movement(keys, current_speed, new_x, new_y)
        
        if self.is_fishing and has_moved:
            self.is_fishing = False
        
        self._reset_collision_state(tile_map)
        self._validate_and_apply_position(new_x, new_y, tile_map)
        self._update_animation(has_moved)
        # Gestionar el sonido de latido si la salud es baja
        self._handle_low_health_sound()

    # Propiedades para compatibilidad con código existente
    @property
    def vida(self):
        return self.health
    
    @vida.setter
    def vida(self, value):
        self.health = value
    
    @property
    def peces_recolectados(self):
        return self.fish_collected
    
    @peces_recolectados.setter
    def peces_recolectados(self, value):
        self.fish_collected = value
    
    @property
    def tiempo_inicio(self):
        return self.start_time
    
    @property
    def pescando(self):
        return self.is_fishing
    
    @property
    def sprite_especial(self):
        return self.show_special_sprite
    
    @property
    def mensaje_pez(self):
        return self.fish_message
    
    @property
    def tiempo_mensaje_pez(self):
        return self.fish_message_timer
    
    @property
    def mensaje_tronco(self):
        return self.collision_message
    
    @property
    def mensaje_turbulencia(self):
        return self.turbulence_message
    
    @property
    def tiempo_mensaje(self):
        return self.turbulence_message_timer
    
    @property
    def colision_tronco(self):
        return self.has_collision
    
    @property
    def tiempo_colision_tronco(self):
        return self.collision_message_timer
    
    @property
    def en_turbulencia(self):
        return self.in_turbulence
    
    @property
    def contador_anim(self):
        return self.animation_counter
    
    def en_agua(self, tile_map):
        return self.is_in_water(tile_map)
    
    def dentro_turbulencia(self, tile_map):
        return self.is_in_turbulence(tile_map)
    
    def buscar_pez_cercano(self, tile_map):
        return self._find_nearby_fish(tile_map)

def encontrar_posicion_inicial(tile_map):
    while True:
        x = random.randint(200, MAP_ANCHO-200)
        y = random.randint(MAP_ALTO-800, MAP_ALTO-200)
        player = Player(x, y)
        if player.is_in_water(tile_map):
            return x, y