from typing import TYPE_CHECKING

import pygame

from src.entities.ghost import Ghost
from src.core.states import GhostState

if TYPE_CHECKING:
    from src.core.game_manager import GameManager

class Blinky(Ghost):

    def __init__(self, x: float, y: float, manager: "GameManager", config: dict, assets: dict):
        super().__init__(x, y, manager, config, assets)

        self._start_mode = GhostState.SCATTER
        self._current_mode = GhostState.SCATTER
        
        self._release_ghost_from_house()

    def _compute_target_tile(self, pacman, all_ghosts) -> tuple[int, int]:
        return pacman._get_grid_coordinates()
    
    def _should_exit_house(self, pacman, all_ghosts) -> bool:
        return True