from src.core.settings import Settings
from src.data.class_config.audio_manager_config import AudioManagerConfig
from src.data.class_config.environment_config import EnvironmentConfig
from src.data.class_config.ghost_config import GhostConfig
from src.data.class_config.hud_config import HUDConfig
from src.data.class_config.pacman_config import PacmanConfig
from src.data.class_config.maze_config import MazeConfig

class ConfigContainer ():

    def __init__ (self) -> None:
        settings = Settings("src/data/settings/config.json")

        self.pacman = PacmanConfig(settings)
        self.ghost = GhostConfig(settings)
        self.environment = EnvironmentConfig(settings)
        self.hud = HUDConfig(settings)
        self.audio_manager = AudioManagerConfig(settings)
        self.maze = MazeConfig(settings)