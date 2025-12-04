from src.core.settings import Settings

class MazeConfig ():

    def __init__ (self, settings: Settings) -> None:
        config = Settings.get("maze", {})
        colors_config = config.get("colors", {})
        radius_config = config.get("radius", {})
        codes_config  = config.get("codes", {})

        self.WALL_COLOR = colors_config.get("wall", "black")
        self.DOOR_COLOR = colors_config.get("door", "black")
        self.SMALL_PELLET_COLOR = colors_config.get("small_pellet", "black")
        self.POWER_PELLET_COLOR = colors_config.get("power_pellet", "black")
        self.SMALL_PELLET_RADIUS = radius_config.get("small_pellet", 1)
        self.POWER_PELLET_RADIUS = radius_config.get("power_pellet", 1)
        self.WALL_CODE_VERTICAL = codes_config.get("vertical", 1)
        self.WALL_CODE_HORIZONTAL = codes_config.get("horizontal", 1)
        self.WALL_CODE_ARC_TL = codes_config.get("arc_tl", 1)
        self.WALL_CODE_ARC_TR = codes_config.get("arc_tr", 1)
        self.WALL_CODE_ARC_BR = codes_config.get("arc_br", 1)
        self.WALL_CODE_ARC_BL = codes_config.get("arc_bl", 1)
        self.WALL_CODE_DOOR = codes_config.get("door", 1)