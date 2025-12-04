from src.core.settings import Settings

class GhostConfig ():

    def __init__(self, settings: Settings) -> None:
        config = Settings.get("ghost")
        
        self.NORMAL_SPEED = config["speed"]["normal"]
        self.EATEN_SPEED = config["speed"]["eaten"]
        self.HOUSE_RESPAWN_TIME_MS = config["spawn_time"]
        
        positions = config["positions"]
        self.SCATTER_TARGET = tuple(positions["scatter_target"])
        self.HOUSE_EXIT_POSITION = tuple(positions["house_exit"])
        self.HOUSE_DOOR_POSITION = tuple(positions["house_door"])
        self.HOUSE_WAIT_POSITION = tuple(positions["house_wait"])