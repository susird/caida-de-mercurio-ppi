import pygame
import sys
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN_MODE

class App:
    def __init__(self):
        pygame.init()
        flags = pygame.FULLSCREEN if FULLSCREEN_MODE else 0
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
        pygame.display.set_caption("Caída de Mercurio")
        self.clock = pygame.time.Clock()

    def show_menu(self):
        from ui.main_menu import MainMenu
        
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
        from core.game import run_game_window
        
        save_game = SaveGame()
        saved_data = save_game.load_saved_game(difficulty)
        
        if saved_data and saved_data.get("has_save", False):
            if self._show_continue_dialog() == "new_game":
                save_game.delete_saved_game(difficulty)
                saved_data = None
        
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
            pygame.quit()
            sys.exit()