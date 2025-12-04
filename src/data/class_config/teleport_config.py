from src.core.settings import Settings

class TeleportConfig ():

    def __init__(self, settings: Settings) -> None:
        teleport = settings.get("teleport")
        self.TELEPORT_MIN_X = teleport["min_x"]
        self.TELEPORT_MAX_X = teleport["max_x"]
        self.TELEPORT_WRAP_X_MIN = teleport["wrap_x_min"]
        self.TELEPORT_WRAP_X_MAX = teleport["wrap_x_max"]