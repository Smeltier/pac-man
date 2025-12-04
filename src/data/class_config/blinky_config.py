from src.core.settings import Settings

class BlinkyConfig ():

    def __init__(self, settings: Settings) -> None:
        config = Settings.get("blinky")
        self.BLINKY_SCATTER_TARGET = tuple(config.get("scatter_target"))