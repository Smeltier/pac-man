import pygame

from src.entities.ghost import Ghost
from src.core.states import GhostState

class Blinky(Ghost):

    def __init__(self, x, y, environment, config: dict, assets: dict):
        super().__init__(x, y, environment, config, assets)

        blinky_config: dict = config.get("blinky")
        self._scatter_target_tile = blinky_config.get("scatter_target")

        self._start_mode = GhostState.SCATTER
        self._current_mode = GhostState.SCATTER

        self._release_ghost_from_house()
        self._exit_timer_ms = 0 

    def _compute_target_tile(self, pacman, all_ghosts) -> tuple[int, int]:
        return pacman._get_grid_coordinates()
    
    def _should_exit_house(self, pacman, all_ghosts) -> bool:
        if self._exit_timer_ms > 0:
            return pygame.time.get_ticks() >= self._exit_timer_ms
        return True