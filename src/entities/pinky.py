import pygame

from src.entities.ghost import Ghost
from src.data.class_config.pinky_config import PinkyConfig

class Pinky (Ghost):

    def __init__(self, x, y, environment, pinky_config: PinkyConfig):
        sprite_paths = {
            1: 'src/images/pinky_up.png',    
            2: 'src/images/pinky_down.png',  
            3: 'src/images/pinky_left.png',  
            4: 'src/images/pinky_right.png', 
        }

        super().__init__(x, y, environment, sprite_paths)

        self.PINKY_SCATTER_TARGET  = pinky_config.PINKY_SCATTER_TARGET
        self.INITIAL_EXIT_DELAY_MS = pinky_config.INITIAL_EXIT_DELAY_MS
        self.CHASE_OFFSET          = pinky_config.CHASE_OFFSET
        
        self.SCATTER_TARGET_TILE = self.PINKY_SCATTER_TARGET
        self._exit_timer_ms = pygame.time.get_ticks() + self.INITIAL_EXIT_DELAY_MS

    def _compute_target_tile(self, pacman, all_ghosts):
        prow, pcol = pacman._get_grid_coordinates()
        
        if pacman._current_orientation == 1:    prow -= self.CHASE_OFFSET
        elif pacman._current_orientation == 2:  prow += self.CHASE_OFFSET
        elif pacman._current_orientation == 3:  pcol -= self.CHASE_OFFSET
        elif pacman._current_orientation == 4:  pcol += self.CHASE_OFFSET
        return (prow, pcol)
    
    def _should_exit_house(self, pacman, all_ghosts) -> bool:
        return pygame.time.get_ticks() >= self._exit_timer_ms