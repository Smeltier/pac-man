from typing import TYPE_CHECKING

import pygame

from src.entities.ghost import Ghost

if TYPE_CHECKING:
    from src.core.game_manager import GameManager

class Pinky(Ghost):

    _chase_offset: int
    _initial_exit_delay_ms: int

    def __init__(self, x: float, y: float, manager: "GameManager", config: dict, assets: dict):
        super().__init__(x, y, manager, config, assets)

        self._initial_exit_delay_ms = config.get("initial_exit_delay", 0)
        self._chase_offset = config.get("chase_offset", 4)
        self._exit_timer_ms = pygame.time.get_ticks() + self._initial_exit_delay_ms

    def _compute_target_tile(self, pacman, all_ghosts) -> tuple[int, int]:
        prow, pcol = pacman._get_grid_coordinates()
        
        if   pacman._current_orientation == 1: prow -= self._chase_offset
        elif pacman._current_orientation == 2: prow += self._chase_offset
        elif pacman._current_orientation == 3: pcol -= self._chase_offset
        elif pacman._current_orientation == 4: pcol += self._chase_offset

        return (prow, pcol)
    
    def _should_exit_house(self, pacman, all_ghosts) -> bool:
        return pygame.time.get_ticks() >= self._exit_timer_ms