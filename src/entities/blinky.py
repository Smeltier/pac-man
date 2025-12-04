import pygame

from src.entities.ghost import Ghost
from src.core.states import GhostState
from src.data.class_config.blinky_config import BlinkyConfig
from src.data.class_config.ghost_config import GhostConfig
from src.data.class_config.teleport_config import TeleportConfig

class Blinky (Ghost):

    def __init__(self, x, y, environment, ghost_config: GhostConfig, blinky_config: BlinkyConfig, teleport_config: TeleportConfig):
        sprite_paths = {
            1: 'src/data/images/blinky_up.png',    
            2: 'src/data/images/blinky_down.png',  
            3: 'src/data/images/blinky_left.png',  
            4: 'src/data/images/blinky_right.png', 
        }

        super().__init__(x, y, environment, sprite_paths, ghost_config, teleport_config)

        self.BLINKY_SCATTER_TARGET = blinky_config.BLINKY_SCATTER_TARGET

        self._start_mode         = GhostState.SCATTER
        self.SCATTER_TARGET_TILE = self.BLINKY_SCATTER_TARGET
        self._current_mode       = GhostState.SCATTER
        self._release_ghost_from_house()
        self._exit_timer_ms      = 0 

    def _compute_target_tile(self, pacman, all_ghosts):
        return pacman._get_grid_coordinates()
    
    def _should_exit_house(self, pacman, all_ghosts) -> bool:
        if self._exit_timer_ms > 0:
            return pygame.time.get_ticks() >= self._exit_timer_ms
        return True