import pygame
from typing import TYPE_CHECKING

from src.entities.ghost import Ghost

if TYPE_CHECKING:
    from src.core.game_manager import GameManager

class Clyde(Ghost):

    _points_required_to_exit: int
    _distance_threshold_squared: int
    
    def __init__(self, x: float, y: float, manager: "GameManager", config: dict, assets: dict):
        super().__init__(x, y, manager, config, assets)

        self._points_required_to_exit = config.get("points_to_exit", 60)
        self._distance_threshold_squared = config.get("distance_threshold_squared", 64)

    def _compute_target_tile(self, pacman, all_ghosts) -> tuple[int, int]:
        prow, pcol = pacman._get_grid_coordinates()
        grow, gcol = self._get_grid_coordinates()

        distance_sq = (prow - grow) ** 2 + (pcol - gcol) ** 2
        
        if distance_sq > self._distance_threshold_squared: 
            return (prow, pcol)
        else: 
            return self._scatter_target_tile

    def _should_exit_house(self, pacman, all_ghosts) -> bool:
        return pacman.total_points >= self._points_required_to_exit