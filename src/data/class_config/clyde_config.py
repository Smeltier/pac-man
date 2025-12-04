from src.core.settings import Settings

class ClydeConfig ():

    def __init__(self, settings: Settings) -> None:
        config: dict = settings.get("clyde", {})
        self.CLYDE_SCATTER_TARGET = tuple(config.get("scatter_target", (0, 0)))
        self.POINTS_TO_EXIT = config.get("points_to_exit", 1)
        self.DISTANCE_THRESHOLD_SQUARED = config.get("distance_threshold_squared", 1)