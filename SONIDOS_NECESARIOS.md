# Sonidos Necesarios para el Juego

## Archivos de sonido requeridos

Coloca los siguientes archivos en la carpeta `assets/sounds/`:

### 1. **game_over.wav** - Sonido de Game Over
- **Descripción**: Se reproduce cuando el jugador pierde (para la música y reproduce este sonido)
- **Sugerencias de búsqueda**: "game over sound", "death sound", "fail sound effect"
- **Duración recomendada**: 2-4 segundos
- **Formato**: WAV o MP3

### 2. **fishing.wav** - Sonido de pescar
- **Descripción**: Se reproduce cuando pescas cualquier tipo de pez
- **Sugerencias de búsqueda**: "fishing sound", "water splash", "catch fish sound"
- **Duración recomendada**: 0.5-1 segundo
- **Formato**: WAV o MP3

### 3. **menu_music.mp3** - Música del menú
- **Descripción**: Música de fondo para el menú principal
- **Sugerencias de búsqueda**: "menu music", "game menu theme", "background music"
- **Duración recomendada**: 2-5 minutos (loop)
- **Formato**: MP3

### 4. **river_ambient.mp3** - Sonido ambiente del río
- **Descripción**: Sonido de fondo durante el juego (flujo de agua)
- **Sugerencias de búsqueda**: "river flowing sound", "water stream ambient", "flowing water loop"
- **Duración recomendada**: 2-5 minutos (loop)
- **Formato**: MP3

## Sitios recomendados para encontrar sonidos gratuitos:

1. **Freesound.org** - Sonidos gratuitos con licencia Creative Commons
2. **Zapsplat.com** - Requiere registro gratuito
3. **Pixabay.com** - Sección de efectos de sonido
4. **OpenGameArt.org** - Recursos para juegos
5. **Mixkit.co** - Efectos de sonido gratuitos

## Instrucciones de instalación:

1. Descarga los archivos de sonido
2. Renómbralos exactamente como se indica arriba
3. Colócalos en la carpeta: `assets/sounds/`
4. El juego los cargará automáticamente al iniciar

## Funcionalidad:

- **menu_music.mp3**: Se reproduce en el menú principal (loop)
- **river_ambient.mp3**: Se reproduce durante el juego (sonido de río en loop)
- **fishing.wav**: Se reproduce cada vez que pescas (cualquier pez)
- **game_over.wav**: Para la música de fondo y reproduce este sonido al perder
- Si un archivo no existe, el juego continuará funcionando sin ese sonido
- Los formatos soportados son WAV y MP3