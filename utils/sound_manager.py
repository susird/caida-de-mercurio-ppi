# utils/sound_manager.py
import pygame
import os
from core.settings import SOUNDS_DIR

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.current_music = None
        self.menu_music_sound = None
        self.river_sound = None
        self.load_sounds()
    
    def load_sounds(self):
        """Carga todos los sonidos del juego"""
        sound_files = {
            'game_over': 'game_over.wav',
            'fishing': 'fishing.mp3'
        }
        
        # Músicas de fondo
        self.music_files = {
            'menu': 'menu_music.mp3',
            'river': 'river_ambient.mp3'
        }
        
        # Cargar músicas como sonidos para reproducir en paralelo
        menu_path = os.path.join(SOUNDS_DIR, 'menu_music.mp3')
        if os.path.exists(menu_path):
            try:
                self.menu_music_sound = pygame.mixer.Sound(menu_path)
            except:
                self.menu_music_sound = None
        
        river_path = os.path.join(SOUNDS_DIR, 'river_ambient.mp3')
        if os.path.exists(river_path):
            try:
                self.river_sound = pygame.mixer.Sound(river_path)
            except:
                self.river_sound = None
        
        for sound_name, filename in sound_files.items():
            sound_path = os.path.join(SOUNDS_DIR, filename)
            if os.path.exists(sound_path):
                try:
                    self.sounds[sound_name] = pygame.mixer.Sound(sound_path)
                except:
                    print(f"Error cargando sonido: {filename}")
                    self.sounds[sound_name] = None
            else:
                self.sounds[sound_name] = None
    
    def play_sound(self, sound_name):
        """Reproduce un sonido"""
        if sound_name in self.sounds and self.sounds[sound_name]:
            self.sounds[sound_name].play()
    
    def play_game_over(self):
        """Para la música y reproduce sonido de game over"""
        self.stop_music()
        self.play_sound('game_over')
    
    def play_music(self, music_name, loop=True):
        """Reproduce música de fondo"""
        if music_name == self.current_music:
            return  # Ya está sonando
            
        music_file = self.music_files.get(music_name)
        if music_file:
            music_path = os.path.join(SOUNDS_DIR, music_file)
            if os.path.exists(music_path):
                try:
                    pygame.mixer.music.load(music_path)
                    pygame.mixer.music.play(-1 if loop else 0)
                    pygame.mixer.music.set_volume(0.3)  # Volumen suave
                    self.current_music = music_name
                except:
                    print(f"Error reproduciendo música: {music_file}")
    
    def stop_music(self):
        """Para la música de fondo"""
        try:
            pygame.mixer.music.stop()
            if self.menu_music_sound:
                self.menu_music_sound.stop()
            if self.river_sound:
                self.river_sound.stop()
            self.current_music = None
        except:
            pass
    
    def play_menu_music(self):
        """Reproduce música del menú"""
        self.play_music('menu')
    
    def play_river_music(self):
        """Reproduce sonido ambiente del río + música del menú muy bajita"""
        self.stop_music()
        
        print(f"DEBUG: river_sound existe: {self.river_sound is not None}")
        print(f"DEBUG: menu_music_sound existe: {self.menu_music_sound is not None}")
        
        # Reproducir ambiente del río en canal 0
        if self.river_sound:
            try:
                channel0 = pygame.mixer.Channel(0)
                self.river_sound.set_volume(0.7)
                channel0.play(self.river_sound, loops=-1)
                print("DEBUG: River sound iniciado")
            except Exception as e:
                print(f"DEBUG: Error river sound: {e}")
        
        # Reproducir música del menú muy bajita en canal 1
        if self.menu_music_sound:
            try:
                channel1 = pygame.mixer.Channel(1)
                self.menu_music_sound.set_volume(0.15)
                channel1.play(self.menu_music_sound, loops=-1)
                print("DEBUG: Menu music iniciado")
            except Exception as e:
                print(f"DEBUG: Error menu music: {e}")
        
        self.current_music = 'river'
    
    def play_fishing(self):
        """Reproduce sonido de pescar"""
        self.play_sound('fishing')
    
    def play_collision(self):
        """Reproduce sonido de colisión"""
        self.play_sound('collision')

# Instancia global del gestor de sonidos
sound_manager = SoundManager()