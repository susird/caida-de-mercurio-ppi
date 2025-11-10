# core/app.py
import pygame
import sys
from core.settings import ANCHO, ALTO, FULLSCREEN

class App:
    def __init__(self):
        pygame.init()
        if FULLSCREEN:
            self.screen = pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Caída de Mercurio")
        self.clock = pygame.time.Clock()

    def show_menu(self):
        """Muestra el menú principal y retorna la acción elegida"""
        from ui.main_menu import MainMenu
        
        main_menu = MainMenu()
        
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return "quit"
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return "quit"
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    accion = main_menu.handle_click(evento.pos)
                    if accion:
                        return accion

            main_menu.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

    def show_game(self, dificultad="novato"):
        """Muestra el juego y retorna cuando termina"""
        from core.game import run_game_window
        return run_game_window(dificultad)

    def run(self):
        """Ejecuta la aplicación"""
        while True:
            accion = self.show_menu()
            
            if accion in ["novato", "medio", "pro"]:
                resultado = self.show_game(accion)
                # Si el juego retorna "menu", continúa el loop
                # Si retorna "quit", sale
                if resultado == "quit":
                    break
            elif accion == "salir" or accion == "quit":
                break
        
        pygame.quit()
        sys.exit()