# Caída de Mercurio

Aventura en aguas envenenadas - Un juego de navegación por ríos contaminados donde debes recolectar 20 peces evitando obstáculos y zonas tóxicas.

## 🎮 Características del Juego

### Modos de Dificultad
- **EXPLORADOR**: 3 minutos para completar la misión
- **AVENTURERO**: 2 minutos para completar la misión
- **SUPERVIVIENTE**: 1 minuto para completar la misión

### Mecánicas de Juego
- **Objetivo**: Recolectar 20 peces antes de que se acabe el tiempo
- **Peces Buenos** (Bocachico, Mojarra, Sábalo, Cucha): Rápidos (3.0-4.5 vel), dan +2 puntos de vida, valen 2 peces
- **Peces Normales** (Tucunaré, Bagre, Dorado, Moncholo): Velocidad media (1.5-2.5), quitan 8 puntos de vida, valen 1 pez
- **Peces con Alto Mercurio**: Lentos (1.0-2.0), quitan 4 puntos de vida, valen 1 pez
- **Obstáculos**: Troncos (80%) y barriles (20%) que quitan vida al chocar
- **Turbulencias**: Zonas de agua contaminada que reducen velocidad y vida gradualmente
- **Dificultad Progresiva**: Los obstáculos se vuelven más rápidos conforme avanzas

### Sistema de Guardado
- **Guardado Automático**: Se guarda al salir con ESC (solo si has pescado al menos 1 pez)
- **Múltiples Partidas**: Cada dificultad mantiene su propia partida guardada
- **Mapas Únicos**: Cada dificultad tiene su propio mapa generado proceduralmente
- **Restauración de Estado**: Posición del jugador, vida, peces recolectados y peces pescados

### Sistema de Instrucciones
- **Pantalla Automática**: Las instrucciones aparecen automáticamente para nuevos jugadores
- **Jugadores Experimentados**: Si tienes una partida guardada con peces pescados, vas directo al juego
- **Interfaz Mejorada**: Fondo oscurecido para mejor legibilidad del texto
- **Botones Horizontales**: Los tres modos de dificultad se muestran en línea horizontal

## 🎯 Controles

- **Flechas (↑↓←→)**: Mover el barco
- **Espacio**: Acelerar (turbo)
- **S**: Pescar (cuando hay peces cerca, radio de 50 píxeles)
- **ESC**: Volver al menú / Guardar partida
- **Click en EMPEZAR A JUGAR**: Iniciar el juego desde las instrucciones
- **Click en X**: Salir del juego

## 🌊 Mundos y Entornos

### Tipos de Terreno
- **Agua Clara**: Navegación normal, velocidad estándar (8 píxeles/frame)
- **Turbulencias**: Agua contaminada con mercurio, velocidad reducida (4 píxeles/frame), pérdida gradual de vida
- **Tierra/Selva**: No navegable, bloquea el movimiento
- **Vegetación**: Árboles, arbustos y flores decorativas

### Generación de Mundo
- **200 peces** distribuidos aleatoriamente en zonas de agua
- **100 obstáculos** iniciales (troncos y barriles)
- **Obstáculos dinámicos** que aparecen según el progreso
- **Mapas únicos** por dificultad usando semillas específicas

## 🏗️ Estructura del Proyecto

```
caida-de-mercurio-main/
├── main.py                 # Punto de entrada principal
├── config/                 # Configuraciones centralizadas
│   ├── __init__.py
│   ├── settings.py        # Configuraciones del sistema (pantalla, colores)
│   └── game_config.py     # Configuraciones del juego (velocidades, peces)
├── core/                   # Lógica principal del juego
│   ├── app.py             # Aplicación principal y menús
│   ├── game_manager.py    # Gestor principal del juego
│   ├── game.py            # Interfaz del juego (legacy)
│   ├── settings.py        # Configuraciones (compatibilidad)
│   └── tile_map.py        # Sistema de mapas y tiles
├── entities/               # Entidades del juego
│   ├── player.py          # Jugador/barco con física y colisiones
│   ├── fish.py            # Peces con diferentes tipos y comportamientos
│   └── obstaculo.py       # Obstáculos (troncos y barriles)
├── ui/                     # Interfaz de usuario
│   ├── main_menu.py       # Menú principal con selección de dificultad
│   ├── instructions_screen.py # Pantalla de instrucciones automática
│   ├── game_screen.py     # Pantalla de juego con cámara
│   ├── game_over_screen.py # Pantalla de derrota
│   ├── win_screen.py      # Pantalla de victoria
│   ├── continue_dialog.py # Diálogo para continuar partidas
│   ├── hud.py             # Interfaz en juego (vida, tiempo, mensajes)
│   └── button.py          # Componente botón reutilizable
├── data/                   # Sistema de persistencia
│   ├── __init__.py
│   ├── game_data.py       # Manejo de estadísticas y puntajes
│   ├── save_game.py       # Sistema de guardado de partidas
│   ├── current_game.json  # Partidas guardadas (generado)
│   ├── scores.json        # Historial de puntajes (generado)
│   ├── progress.json      # Progreso por dificultad (generado)
│   └── stats.json         # Estadísticas generales (generado)
├── utils/                  # Utilidades y helpers
│   ├── constants.py       # Constantes del juego
│   ├── helpers.py         # Funciones auxiliares
│   ├── fish_sprites.py    # Generación procedural de sprites de peces
│   ├── jungle_sprites.py  # Sprites de vegetación de selva
│   ├── tile_generator.py  # Generador de tiles de terreno
│   ├── tree_loader.py     # Cargador de sprites de árboles
│   └── obstacle_loader.py # Cargador de sprites de obstáculos
├── assets/                 # Recursos gráficos
│   ├── images/            # Sprites y texturas
│   │   ├── navegante_rio1.png, navegante_rio2.png # Sprites del barco
│   │   ├── navegante_caido.png # Sprite de colisión
│   │   ├── tronco.png, barril.png # Obstáculos
│   │   ├── tree1-9.png    # Árboles
│   │   ├── arbusto1-6.png # Arbustos
│   │   ├── roca1-6.png    # Rocas
│   │   ├── Map_tile_*.png # Tiles de terreno
│   │   └── fondo_*.png    # Fondos de pantallas
│   └── sounds/            # Audio (no implementado)
└── fonts/                  # Fuentes tipográficas
    ├── Airstream.ttf      # Fuente principal
    ├── Anagram.ttf        # Fuente alternativa
    └── VT323-Regular.ttf  # Fuente de interfaz
```

## 💾 Sistema de Datos

El juego genera automáticamente archivos JSON para persistir datos:

- **current_game.json**: Partidas guardadas por dificultad con posición, vida, peces recolectados
- **scores.json**: Historial de puntajes con tiempo y resultado
- **progress.json**: Progreso y mejores tiempos por dificultad
- **stats.json**: Estadísticas generales (partidas jugadas, peces totales, etc.)

## 🚀 Instalación y Ejecución

### Requisitos
- Python 3.6 o superior
- Pygame 2.0 o superior

### Instalación
```bash
# Instalar Pygame
pip install pygame

# Clonar o descargar el proyecto
# Navegar al directorio del proyecto
cd caida-de-mercurio-main
```

### Ejecución
```bash
# Ejecutar el juego
python main.py

# O en algunos sistemas
python3 main.py
```

## 🎨 Características Técnicas

### Arquitectura
- **Patrón MVC**: Separación clara entre lógica, datos y presentación
- **Arquitectura Modular**: Código organizado en módulos especializados
- **Sistema de Configuración**: Configuraciones centralizadas en `config/`
- **Manejo de Estados**: Sistema robusto de guardado y carga de partidas

### Rendimiento
- **Generación Procedural**: Mapas únicos por dificultad usando semillas específicas
- **Optimización de Renderizado**: Solo dibuja elementos visibles en cámara
- **Gestión de Memoria**: Reutilización de sprites y recursos
- **60 FPS**: Bucle de juego optimizado para 60 fotogramas por segundo

### Escalabilidad
- **Sistema de Plugins**: Fácil adición de nuevos tipos de peces y obstáculos
- **Configuración Externa**: Parámetros modificables sin tocar código
- **Arquitectura Extensible**: Preparada para futuras expansiones

## 🏆 Mecánicas de Juego Detalladas

### Sistema de Vida
- **Vida inicial**: 100 puntos
- **Peces buenos**: Restauran 2 puntos de vida
- **Peces tóxicos**: Quitan 4-8 puntos de vida
- **Turbulencias**: Pérdida gradual de 0.05 puntos por frame
- **Obstáculos**: Quitan 1-2 puntos según el contexto

### Sistema de Pesca
- **Radio de pesca**: 50 píxeles alrededor del barco
- **Tecla de acción**: S para pescar
- **Tipos de peces**: 70% buenos en turbulencias, 15% buenos en agua normal
- **Mensajes informativos**: Feedback visual del tipo de pez pescado

### Sistema de Movimiento
- **Velocidad normal**: 8 píxeles por frame
- **Velocidad en turbulencias**: 4 píxeles por frame
- **Velocidad con turbo**: 15 píxeles por frame
- **Efectos de turbulencia**: Movimiento errático adicional

### Cámara y Visualización
- **Cámara que sigue**: Centrada en el jugador
- **Límites de mapa**: Cámara limitada a los bordes del mundo
- **HUD informativo**: Vida, peces recolectados, tiempo restante
- **Mensajes contextuales**: Información sobre pesca y colisiones

## 🎯 Flujo de Juego

### Para Nuevos Jugadores
1. **Menú Principal** → Seleccionar dificultad (botones horizontales)
2. **Pantalla de Instrucciones** → Leer cómo jugar automáticamente
3. **Empezar a Jugar** → Iniciar el juego con la dificultad elegida

### Para Jugadores con Progreso
1. **Menú Principal** → Seleccionar dificultad
2. **Diálogo de Continuar** → Continuar partida guardada o empezar nueva
3. **Si elige nueva partida** → Ver instrucciones → Jugar

## 🎯 Objetivos y Estrategias

1. **Supervivencia**: Mantén tu vida evitando peces tóxicos y obstáculos
2. **Recolección Eficiente**: Pesca 20 peces priorizando los buenos
3. **Gestión de Tiempo**: Usa el turbo sabiamente para optimizar rutas
4. **Estrategia de Turbulencias**: Busca peces buenos en zonas contaminadas
5. **Progresión**: Domina las tres dificultades para completar el desafío

## 🐟 Tipos de Peces

| Tipo | Especies | Velocidad | Efecto en Vida | Valor |
|------|----------|-----------|----------------|-------|
| Buenos | Bocachico, Mojarra, Sábalo, Cucha | 3.0-4.5 | +2 puntos | 2 peces |
| Normales | Tucunaré, Bagre, Dorado, Moncholo | 1.5-2.5 | -8 puntos | 1 pez |
| Alto Mercurio | Tucunaré, Bagre, Dorado, Moncholo | 1.0-2.0 | -4 puntos | 1 pez |

## 🚧 Obstáculos

- **Troncos**: 80% de probabilidad, obstáculos naturales
- **Barriles**: 20% de probabilidad, contaminación industrial
- **Generación dinámica**: Aparecen más obstáculos según el progreso
- **Colisiones**: Causan daño y mensaje informativo

---

**Desarrollado con ❤️ usando Python y Pygame**

*Un juego sobre la contaminación por mercurio en los ríos y la importancia de la conservación acuática.*
