from src.core.settings import Settings

class PinkyConfig ():

    def __init__(self, settings: Settings) -> None:
        config = Settings.get("pinky")
        self.PINKY_SCATTER_TARGET = tuple(config.get("scatter_target"))
        self.INITIAL_EXIT_DELAY_MS = config.get("initial_exit_delay")
        self.CHASE_OFFSET = config.get("chase_offset")