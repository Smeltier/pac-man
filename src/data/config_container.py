from src.core.settings                          import Settings
from src.data.class_config.audio_manager_config import AudioManagerConfig
from src.data.class_config.environment_config   import EnvironmentConfig
from src.data.class_config.ghost_config         import GhostConfig
from src.data.class_config.hud_config           import HUDConfig
from src.data.class_config.pacman_config        import PacmanConfig
from src.data.class_config.maze_config          import MazeConfig
from src.data.class_config.blinky_config        import BlinkyConfig
from src.data.class_config.clyde_config         import ClydeConfig
from src.data.class_config.inky_config          import InkyConfig
from src.data.class_config.pinky_config         import PinkyConfig
from src.data.class_config.teleport_config      import TeleportConfig

class ConfigContainer ():

    def __init__ (self) -> None:
        settings = Settings("src/data/settings/config.json")

        self.audio_manager = AudioManagerConfig(settings)
        self.environment   = EnvironmentConfig(settings)
        self.teleport = TeleportConfig(settings)
        self.pacman        = PacmanConfig(settings)
        self.blinky        = BlinkyConfig(settings)
        self.ghost         = GhostConfig(settings)
        self.pinky         = PinkyConfig(settings)
        self.clyde         = ClydeConfig(settings)
        self.maze          = MazeConfig(settings)
        self.inky          = InkyConfig(settings)
        self.hud           = HUDConfig(settings)