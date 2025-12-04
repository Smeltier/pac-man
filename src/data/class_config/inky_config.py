from src.core.settings import Settings

class InkyConfig ():

    def __init__(self, settings: Settings) -> None:
        config = settings.get("inky")
        self.INKY_SCATTER_TARGET = tuple(config.get("scatter_target"))
        self.POINTS_TO_EXIT = config.get("points_to_exit")
        self.CHASE_OFFSET = config.get("chase_offset")