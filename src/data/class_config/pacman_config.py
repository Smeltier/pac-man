from src.core.settings import Settings

class PacmanConfig:

    def __init__ (self, settings) -> None:
        config: dict = settings.get("pacman", {})

        self.SPEED = config.get("speed", 1)
        self.ANIMATION_SPEED_SECONDS = config.get("animation_speed_seconds", 0.1)
        self.COLLISION_RECT_SIZE = config.get("collision_rect_size", 1)

        points_config: dict = config.get("points", {})

        self.SMALL_PELLET_POINTS = points_config.get("small_pellet", 1)
        self.POWER_PELLET_POINTS = points_config.get("power_pellet", 1)
        self.GHOST_BASE_POINTS = points_config.get("ghost_base", 1)