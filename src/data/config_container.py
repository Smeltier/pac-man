from src.core.settings import Settings
from src.data.audio_manager_config import AudioManagerConfig
from src.data.environment_config import EnvironmentConfig
from src.data.ghost_config import GhostConfig
from src.data.hud_config import HUDCOnfig
from src.data.pacman_config import PacmanConfig
from src.data.maze_config import MazeConfig

class ConfigContainer ():

    def __init__ (self) -> None:
        settings = Settings("src/data/settings/config.json")

        self.pacman = PacmanConfig(settings)
        self.ghost = GhostConfig(settings)
        self.environment = EnvironmentConfig(settings)
        self.hud = HUDCOnfig(settings)
        self.audio_manager = AudioManagerConfig(settings)
        self.maze = MazeConfig(settings)