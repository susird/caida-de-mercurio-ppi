import pygame
import sys
from core.settings import ANCHO, ALTO, FULLSCREEN
from ui.main_menu import MainMenu
from core.game import run_game

if __name__ == '__main__':
    pygame.init()
    if FULLSCREEN:
        pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN)
    else:
        pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Caída de Mercurio")

    clock = pygame.time.Clock()
    main_menu = MainMenu()

    # Pantalla de inicio
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            # Detectar clic sobre los botones
            if evento.type == pygame.MOUSEBUTTONDOWN:
                accion = main_menu.handle_click(evento.pos)
                if accion == "jugar":
                    esperando = False  # Salimos de la pantalla de inicio
                elif accion == "salir":
                    pygame.quit()
                    sys.exit()

        # Dibujar la ventana
        main_menu.draw(pantalla)
        pygame.display.flip()
        clock.tick(60)

    # Aquí empieza el juego normal
    run_game()
