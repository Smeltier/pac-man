from src.core.settings import Settings

class EnvironmentConfig ():

    def __init__(self, settings: Settings) -> None:
        config: dict = settings.get("environment", {})
        duration_config = config.get("duration_ms", {})

        self.INITIAL_LIVES = config.get("initial_lives", 1)
        self.VULNERABLE_DURATION_MS = duration_config.get("vulnerable", 1)
        self.CHASE_DURATION_MS = duration_config.get("chase", 1)
        self.SCATTER_DURATION_MS = duration_config.get("scatter", 1)
        self.GAME_OVER_SCREEN_DURATION_MS = duration_config.get("game_over_screen", 1)