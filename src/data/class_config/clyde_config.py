from src.core.settings import Settings

class ClydeConfig ():

    def __init__(self, settings: Settings) -> None:
        config = Settings.get("clyde")
        self.CLYDE_SCATTER_TARGET = tuple(config.get("scatter_target"))
        self.POINTS_TO_EXIT = config.get("points_to_exit")
        self.DISTANCE_THRESHOLD_SQUARED = config.get("distance_threshold_squared")