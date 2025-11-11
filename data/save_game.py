import json
import os
from pathlib import Path

class SaveGame:
    def __init__(self):
        self.data_dir = Path(__file__).parent
        self.save_file = self.data_dir / "current_game.json"
    
    def save_current_game(self, difficulty, player_data, elapsed_time, fished_positions=None):
        """Guarda el estado actual del juego"""
        # Cargar todas las partidas guardadas
        all_saves = self._load_all_saves()
        
        # Actualizar o agregar la partida de esta dificultad
        save_data = {
            "difficulty": difficulty,
            "player_x": player_data.x,
            "player_y": player_data.y,
            "health": player_data.health,
            "fish_collected": player_data.fish_collected,
            "elapsed_time": elapsed_time,
            "has_save": True
        }
        
        if fished_positions:
            save_data["fished_positions"] = fished_positions
        
        all_saves[difficulty] = save_data
        
        try:
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(all_saves, f, indent=2)
        except Exception as e:
            print(f"Error guardando partida: {e}")
    
    def load_saved_game(self, difficulty=None):
        """Carga la partida guardada de una dificultad específica"""
        all_saves = self._load_all_saves()
        if difficulty and difficulty in all_saves:
            return all_saves[difficulty]
        return None
    
    def _load_all_saves(self):
        """Carga todas las partidas guardadas"""
        try:
            if self.save_file.exists():
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Compatibilidad con formato anterior
                    if isinstance(data, dict) and "difficulty" in data:
                        # Formato anterior: convertir a nuevo formato
                        difficulty = data["difficulty"]
                        return {difficulty: data}
                    return data
        except Exception as e:
            print(f"Error cargando partidas: {e}")
        return {}
    
    def has_saved_game(self, difficulty=None):
        """Verifica si hay una partida guardada para una dificultad"""
        if difficulty:
            save_data = self.load_saved_game(difficulty)
            return save_data is not None and save_data.get("has_save", False)
        else:
            all_saves = self._load_all_saves()
            return len(all_saves) > 0
    
    def delete_saved_game(self, difficulty=None):
        """Elimina la partida guardada de una dificultad específica"""
        try:
            if difficulty:
                all_saves = self._load_all_saves()
                if difficulty in all_saves:
                    del all_saves[difficulty]
                    if all_saves:
                        with open(self.save_file, 'w', encoding='utf-8') as f:
                            json.dump(all_saves, f, indent=2)
                    else:
                        # Si no quedan partidas, eliminar archivo
                        if self.save_file.exists():
                            os.remove(self.save_file)
            else:
                # Eliminar todas las partidas
                if self.save_file.exists():
                    os.remove(self.save_file)
        except Exception as e:
            print(f"Error eliminando partida: {e}")