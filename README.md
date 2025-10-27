# Caída de Mercurio

Aventura en aguas envenenadas - Un juego de navegación por ríos contaminados.

## Estructura del Proyecto

```
caida-de-mercurio/
├── main.py                 # Punto de entrada del juego
├── core/                   # Lógica principal del juego
│   ├── game.py            # Game loop y generación de mapas
│   └── settings.py        # Configuraciones globales
├── ui/                     # Interfaz de usuario
│   ├── main_menu.py       # Menú principal
│   ├── game_screen.py     # Pantalla de juego
│   └── button.py          # Componente botón reutilizable
├── entities/               # Entidades del juego
│   └── player.py          # Lógica del jugador/barco
├── utils/                  # Utilidades y helpers
│   ├── constants.py       # Constantes del juego
│   └── helpers.py         # Funciones auxiliares
├── assets/                 # Recursos del juego
│   ├── images/            # Imágenes y sprites
│   └── sounds/            # Efectos de sonido y música
├── fonts/                  # Fuentes tipográficas
└── README.md              # Este archivo
```

## Controles

- **Flechas**: Mover el barco
- **Espacio**: Acelerar (turbo)

## Características

- Navegación por ríos generados proceduralmente
- Zonas de turbulencia que afectan el movimiento
- Sistema de cámara que sigue al jugador
- Animación del barco con múltiples frames

## Requisitos

- Python 3.x
- Pygame

## Instalación y Ejecución

```bash
pip install pygame
python main.py
```