import pygame

from src.entities.ghost import Ghost
from src.states import GhostState

class Blinky (Ghost):

    def __init__(self, x, y, environment):
        sprite_paths = {
            1: 'src/images/blinky_up.png',    
            2: 'src/images/blinky_down.png',  
            3: 'src/images/blinky_left.png',  
            4: 'src/images/blinky_right.png', 
        }

        super().__init__(x, y, environment, sprite_paths)

        self.start_mode = GhostState.SCATTER
        self.scatter_target = (2, 27)
        self.mode = GhostState.SCATTER
        self._release_ghost()
        self._exit_timer = 0 

    def _compute_target(self, pacman, all_ghosts):
        return pacman._get_coordinates()
    
    def _should_exit_house(self, pacman, all_ghosts) -> bool:
        if self._exit_timer > 0:
            return pygame.time.get_ticks() >= self._exit_timer
        return True

class Pinky (Ghost):
    def __init__(self, x, y, environment):
        sprite_paths = {
            1: 'src/images/pinky_up.png',    
            2: 'src/images/pinky_down.png',  
            3: 'src/images/pinky_left.png',  
            4: 'src/images/pinky_right.png', 
        }

        super().__init__(x, y, environment, sprite_paths)
        
        self.scatter_target = (2, 2)
        self._exit_timer = pygame.time.get_ticks() + 500

    def _compute_target(self, pacman, all_ghosts):
        prow, pcol = pacman._get_coordinates()
        
        if pacman._current_orientation == 1:    prow -= 4
        elif pacman._current_orientation == 2:  prow += 4
        elif pacman._current_orientation == 3:  pcol -= 4
        elif pacman._current_orientation == 4:  pcol += 4
        return (prow, pcol)
    
    def _should_exit_house(self, pacman, all_ghosts) -> bool:
        return pygame.time.get_ticks() >= self._exit_timer

class Inky (Ghost):
    def __init__(self, x, y, environment):
        sprite_paths = {
            1: 'src/images/inky_up.png',    
            2: 'src/images/inky_down.png',  
            3: 'src/images/inky_left.png',  
            4: 'src/images/inky_right.png', 
        }

        super().__init__(x, y, environment, sprite_paths)
        
        self.scatter_target = (30, 27) 
        self.points_to_exit = 30

    def _compute_target(self, pacman, all_ghosts):
        blinky = self.get_ghost(all_ghosts, Blinky)
        if not blinky:
            return pacman._get_coordinates()
        
        brow, bcol = blinky._get_coordinates()
        prow, pcol = pacman._get_coordinates()
        
        if pacman._current_orientation == 1:    prow -= 2
        elif pacman._current_orientation == 2:  prow += 2
        elif pacman._current_orientation == 3:  pcol -= 2
        elif pacman._current_orientation == 4:  pcol += 2

        target_row = 2 * prow - brow
        target_col = 2 * pcol - bcol
        return (target_row, target_col)
    
    def _should_exit_house(self, pacman, all_ghosts) -> bool:
        return pacman.total_points >= self.points_to_exit

class Clyde (Ghost):
    def __init__(self, x, y, environment):
        sprite_paths = {
            1: 'src/images/clyde_up.png',    
            2: 'src/images/clyde_down.png',  
            3: 'src/images/clyde_left.png',  
            4: 'src/images/clyde_right.png', 
        }
        
        super().__init__(x, y, environment, sprite_paths)
        
        self.scatter_target = (30, 2)
        self.points_to_exit = 60

    def _compute_target(self, pacman, all_ghosts):
        prow, pcol = pacman._get_coordinates()
        grow, gcol = self._get_coordinates()

        distance_sq = (prow - grow)**2 + (pcol - gcol)**2
        if distance_sq > 64: 
            return (prow, pcol)
        else: 
            return self.scatter_target

    def _should_exit_house(self, pacman, all_ghosts) -> bool:
        return pacman.total_points >= self.points_to_exit