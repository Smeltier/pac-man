from typing import TYPE_CHECKING

import pygame

from src.entities.blinky import Blinky
from src.entities.ghost import Ghost

if TYPE_CHECKING:
    from src.core.game_manager import GameManager

class Inky(Ghost):
    
    def __init__(self, x: float, y: float, manager: "GameManager", config: dict, assets: dict):
        super().__init__(x, y, manager, config, assets)

        self._chase_offset = config.get("chase_offset", 2)
        self._points_required_to_exit = config.get("points_to_exit", 30)

    def _compute_target_tile(self, pacman, all_ghosts) -> tuple[int, int]:
        blinky = next((g for g in all_ghosts if isinstance(g, Blinky)), None)
        
        if not blinky:
            return pacman._get_grid_coordinates()
        
        brow, bcol = blinky._get_grid_coordinates()
        prow, pcol = pacman._get_grid_coordinates()
        
        if   pacman._current_orientation == 1: prow -= self._chase_offset
        elif pacman._current_orientation == 2: prow += self._chase_offset
        elif pacman._current_orientation == 3: pcol -= self._chase_offset
        elif pacman._current_orientation == 4: pcol += self._chase_offset

        target_row = 2 * prow - brow
        target_col = 2 * pcol - bcol
        
        return (target_row, target_col)
    
    def _should_exit_house(self, pacman, all_ghosts) -> bool:
        return pacman.total_points >= self._points_required_to_exit