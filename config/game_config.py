BOAT_SPEED_NORMAL = 8
BOAT_SPEED_TURBULENCE = 4
BOAT_SPEED_BOOST = 15

BOAT_WIDTH = 90
BOAT_HEIGHT = 70

UI_CREAM = (255, 243, 196)
UI_BLACK = (0, 0, 0)
UI_ORANGE = (255, 180, 70)

DIFFICULTY_SETTINGS = {
    "novato": {"time_limit": 180, "fish_goal": 20},
    "medio": {"time_limit": 120, "fish_goal": 20},
    "pro": {"time_limit": 60, "fish_goal": 20}
}

FISH_TYPES = {
    "good": {
        "names": ["Bocachico", "Mojarra", "Sábalo", "Cucha"],
        "speed_range": (3.0, 4.5),
        "health_effect": -2,
        "score_value": 2
    },
    "normal": {
        "names": ["Tucunaré", "Bagre", "Dorado", "Moncholo"],
        "speed_range": (1.5, 2.5),
        "health_effect": 8,
        "score_value": 1
    },
    "high_mercury": {
        "names": ["Tucunaré", "Bagre", "Dorado", "Moncholo"],
        "speed_range": (1.0, 2.0),
        "health_effect": 4,
        "score_value": 1
    }
}