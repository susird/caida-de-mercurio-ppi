# core/game_manager.py
import pygame
import sys
from core.settings import ANCHO, ALTO, FULLSCREEN
from ui.main_menu import MainMenu
from core.game import run_game

class GameState:
    MENU = "menu"
    PLAYING = "playing"
    QUIT = "quit"

class GameManager:
    def __init__(self):
        pygame.init()
        if FULLSCREEN:
            self.screen = pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Caída de Mercurio")
        
        self.clock = pygame.time.Clock()
        self.main_menu = MainMenu()
        self.state = GameState.MENU
        self.running = True

    def handle_menu_events(self):
        """Maneja eventos del menú principal"""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.state = GameState.QUIT
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.state = GameState.QUIT
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                accion = self.main_menu.handle_click(evento.pos)
                if accion == "jugar":
                    self.state = GameState.PLAYING
                elif accion == "salir":
                    self.state = GameState.QUIT

    def run_menu(self):
        """Ejecuta el menú principal"""
        while self.state == GameState.MENU:
            self.handle_menu_events()
            
            if self.state == GameState.MENU:
                self.main_menu.draw(self.screen)
                pygame.display.flip()
                self.clock.tick(60)

    def run_game_loop(self):
        """Ejecuta el juego y regresa al menú cuando termina"""
        run_game()
        self.state = GameState.MENU  # Volver al menú después del juego

    def run(self):
        """Loop principal del juego"""
        while self.running:
            if self.state == GameState.MENU:
                self.run_menu()
            elif self.state == GameState.PLAYING:
                self.run_game_loop()
            elif self.state == GameState.QUIT:
                self.running = False
        
        pygame.quit()
        sys.exit()