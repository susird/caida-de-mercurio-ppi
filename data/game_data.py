import json
import os
from datetime import datetime
from pathlib import Path

class GameData:
    def __init__(self):
        self.data_dir = Path(__file__).parent
        self.scores_file = self.data_dir / "scores.json"
        self.progress_file = self.data_dir / "progress.json"
        self.stats_file = self.data_dir / "stats.json"
        
        self._init_files()
    
    def _init_files(self):
        """Inicializa archivos de datos si no existen"""
        if not self.scores_file.exists():
            self._create_scores_file()
        
        if not self.progress_file.exists():
            self._create_progress_file()
        
        if not self.stats_file.exists():
            self._create_stats_file()
    
    def _create_scores_file(self):
        """Crea archivo de puntajes"""
        initial_scores = {
            "high_scores": [],
            "last_updated": datetime.now().isoformat()
        }
        self._save_json(self.scores_file, initial_scores)
    
    def _create_progress_file(self):
        """Crea archivo de progreso"""
        initial_progress = {
            "levels_completed": {
                "novato": False,
                "medio": False,
                "pro": False
            },
            "best_times": {
                "novato": None,
                "medio": None,
                "pro": None
            },
            "total_games_played": 0,
            "last_played": None
        }
        self._save_json(self.progress_file, initial_progress)
    
    def _create_stats_file(self):
        """Crea archivo de estadísticas"""
        initial_stats = {
            "total_fish_caught": 0,
            "total_obstacles_hit": 0,
            "total_time_played": 0,
            "games_won": 0,
            "games_lost": 0,
            "best_fish_streak": 0
        }
        self._save_json(self.stats_file, initial_stats)
    
    def _save_json(self, file_path, data):
        """Guarda datos en archivo JSON"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando {file_path}: {e}")
    
    def _load_json(self, file_path):
        """Carga datos desde archivo JSON"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error cargando {file_path}: {e}")
            return {}
    
    def save_score(self, difficulty, fish_caught, time_taken, won, player_name="Jugador"):
        """Guarda un puntaje"""
        scores_data = self._load_json(self.scores_file)
        
        score_entry = {
            "player_name": player_name,
            "difficulty": difficulty,
            "fish_caught": fish_caught,
            "time_taken": time_taken,
            "won": won,
            "date": datetime.now().isoformat(),
            "score": self._calculate_score(fish_caught, time_taken, won, difficulty)
        }
        
        scores_data["high_scores"].append(score_entry)
        scores_data["high_scores"].sort(key=lambda x: x["score"], reverse=True)
        scores_data["high_scores"] = scores_data["high_scores"][:10]  # Top 10
        scores_data["last_updated"] = datetime.now().isoformat()
        
        self._save_json(self.scores_file, scores_data)
    
    def _calculate_score(self, fish_caught, time_taken, won, difficulty):
        """Calcula puntaje basado en rendimiento"""
        base_score = fish_caught * 100
        
        if won:
            base_score += 1000
            # Bonus por tiempo restante
            time_limits = {"novato": 180, "medio": 120, "pro": 60}
            time_bonus = max(0, time_limits[difficulty] - time_taken) * 10
            base_score += time_bonus
        
        # Multiplicador por dificultad
        difficulty_multiplier = {"novato": 1.0, "medio": 1.5, "pro": 2.0}
        base_score *= difficulty_multiplier[difficulty]
        
        return int(base_score)
    
    def update_progress(self, difficulty, time_taken, won):
        """Actualiza progreso del jugador"""
        progress_data = self._load_json(self.progress_file)
        
        progress_data["total_games_played"] += 1
        progress_data["last_played"] = datetime.now().isoformat()
        
        if won:
            progress_data["levels_completed"][difficulty] = True
            
            current_best = progress_data["best_times"][difficulty]
            if current_best is None or time_taken < current_best:
                progress_data["best_times"][difficulty] = time_taken
        
        self._save_json(self.progress_file, progress_data)
    
    def update_stats(self, fish_caught, obstacles_hit, time_played, won):
        """Actualiza estadísticas generales"""
        stats_data = self._load_json(self.stats_file)
        
        stats_data["total_fish_caught"] += fish_caught
        stats_data["total_obstacles_hit"] += obstacles_hit
        stats_data["total_time_played"] += time_played
        
        if won:
            stats_data["games_won"] += 1
        else:
            stats_data["games_lost"] += 1
        
        if fish_caught > stats_data["best_fish_streak"]:
            stats_data["best_fish_streak"] = fish_caught
        
        self._save_json(self.stats_file, stats_data)
    
    def get_high_scores(self):
        """Obtiene los mejores puntajes"""
        return self._load_json(self.scores_file).get("high_scores", [])
    
    def get_best_times(self):
        """Obtiene los mejores tiempos (solo victorias)"""
        all_scores = self._load_json(self.scores_file).get("high_scores", [])
        # Filtrar solo victorias y ordenar por tiempo (menor es mejor)
        victories = [score for score in all_scores if score.get("won", False)]
        victories.sort(key=lambda x: x.get("time_taken", 999))
        return victories[:5]
    
    def get_progress(self):
        """Obtiene el progreso del jugador"""
        return self._load_json(self.progress_file)
    
    def get_stats(self):
        """Obtiene las estadísticas del jugador"""
        return self._load_json(self.stats_file)