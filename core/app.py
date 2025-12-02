import pygame
import sys
import os
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN_MODE, SOUNDS_DIR

class App:
    def __init__(self):
        pygame.init()
        # Inicializar el mezclador de sonido (módulo de audio)
        try:
            pygame.mixer.init()
        except Exception as e:
            # Si falla la inicialización del mezclador, no bloqueamos el juego
            print(f"Advertencia: no se pudo inicializar el mezclador de audio: {e}")
        flags = pygame.FULLSCREEN if FULLSCREEN_MODE else 0
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
        pygame.display.set_caption("Caída de Mercurio")
        self.clock = pygame.time.Clock()
        # Reproducir música de fondo en loop contínuo (si existe el archivo)
        try:
            music_file = SOUNDS_DIR / "BackgroudMusic.mp3"
            if music_file.exists():
                pygame.mixer.music.load(str(music_file))
                pygame.mixer.music.set_volume(0.5)  # ajustar volumen por defecto
                pygame.mixer.music.play(-1)  # -1 para repetir infinitamente
            else:
                print(f"Aviso: archivo de música no encontrado: {music_file}")
        except Exception as e:
            print(f"Advertencia: no se pudo reproducir la música de fondo: {e}")

    def show_menu(self):
        from ui.main_menu import MainMenu
        from utils.sound_manager import sound_manager
        
        # Reproducir música del menú
        sound_manager.play_menu_music()
        
        main_menu = MainMenu()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return "quit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    action = main_menu.handle_click(event.pos)
                    if action:
                        return action
            
            main_menu.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

    def show_game(self, difficulty="novato"):
        from data.save_game import SaveGame
        from core.game_manager import run_game_window
        
        save_game = SaveGame()
        saved_data = save_game.load_saved_game(difficulty)
        
        if saved_data and saved_data.get("has_save", False):
            choice = self._show_continue_dialog()
            if choice == "new_game":
                save_game.delete_saved_game(difficulty)
                return self.show_instructions(difficulty)
        # Cambiar a música del río al iniciar el juego
        from utils.sound_manager import sound_manager
        sound_manager.play_river_music()
        
        return run_game_window(difficulty, saved_data)
    
    def _show_continue_dialog(self):
        from ui.continue_dialog import ContinueDialog
        from ui.main_menu import MainMenu
        
        dialog = ContinueDialog()
        main_menu = MainMenu()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return "new_game"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    choice = dialog.handle_click(event.pos)
                    if choice:
                        return choice
            
            main_menu.draw(self.screen)
            dialog.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

    def show_instructions(self, difficulty):
        from ui.instructions_screen import InstructionsScreen
        
        instructions_screen = InstructionsScreen()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return "menu"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    action = instructions_screen.handle_click(event.pos)
                    if action == "start_game":
                        return self.show_game(difficulty)
            
            instructions_screen.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
    
    def run(self):
        try:
            while True:
                action = self.show_menu()
                
                if action in ["novato", "medio", "pro"]:
                    # Verificar si hay partida guardada válida (con al menos 1 pez pescado)
                    from data.save_game import SaveGame
                    save_game = SaveGame()
                    saved_data = save_game.load_saved_game(action)
                    
                    if saved_data and saved_data.get("has_save", False) and saved_data.get("fish_collected", 0) > 0:
                        # Hay partida guardada válida, ir directo al juego
                        result = self.show_game(action)
                    else:
                        # No hay partida guardada válida, mostrar instrucciones primero
                        result = self.show_instructions(action)
                    
                    if result == "quit":
                        break
                elif action in ["salir", "quit"]:
                    break
        finally:
            # Parar la música y desinicializar el mezclador si está activo
            try:
                if pygame.mixer.get_init():
                    pygame.mixer.music.stop()
                    pygame.mixer.quit()
            except Exception:
                pass
            pygame.quit()
            sys.exit()