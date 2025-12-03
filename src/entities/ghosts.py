import pygame

from src.entities.ghost import Ghost
from src.core.states import GhostState
from src.core.settings import Settings

class Blinky (Ghost):

    def __init__(self, x, y, environment):
        sprite_paths = {
            1: 'src/images/blinky_up.png',    
            2: 'src/images/blinky_down.png',  
            3: 'src/images/blinky_left.png',  
            4: 'src/images/blinky_right.png', 
        }

        super().__init__(x, y, environment, sprite_paths)

        self._initial_config()

        self._start_mode = GhostState.SCATTER
        self.SCATTER_TARGET_TILE = self.BLINKY_SCATTER_TARGET
        self._current_mode = GhostState.SCATTER
        self._release_ghost_from_house()
        self._exit_timer_ms = 0 

    def _compute_target_tile(self, pacman, all_ghosts):
        return pacman._get_grid_coordinates()
    
    def _should_exit_house(self, pacman, all_ghosts) -> bool:
        if self._exit_timer_ms > 0:
            return pygame.time.get_ticks() >= self._exit_timer_ms
        return True
    
    def _initial_config (self) -> None:
        super()._initial_config()
        config = Settings.get("blinky")
        self.BLINKY_SCATTER_TARGET = tuple(config.get("scatter_target"))

class Pinky (Ghost):

    def __init__(self, x, y, environment):
        sprite_paths = {
            1: 'src/images/pinky_up.png',    
            2: 'src/images/pinky_down.png',  
            3: 'src/images/pinky_left.png',  
            4: 'src/images/pinky_right.png', 
        }

        super().__init__(x, y, environment, sprite_paths)
        
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
    
    def _initial_config (self) -> None:
        super()._initial_config()
        config = Settings.get("pinky")
        self.PINKY_SCATTER_TARGET = tuple(config.get("scatter_target"))
        self.INITIAL_EXIT_DELAY_MS = config.get("initial_exit_delay")
        self.CHASE_OFFSET = config.get("chase_offset")

class Inky (Ghost):
    
    def __init__(self, x, y, environment):
        sprite_paths = {
            1: 'src/images/inky_up.png',    
            2: 'src/images/inky_down.png',  
            3: 'src/images/inky_left.png',  
            4: 'src/images/inky_right.png', 
        }

        super().__init__(x, y, environment, sprite_paths)
        
        self.SCATTER_TARGET_TILE = self.INKY_SCATTER_TARGET
        self._points_required_to_exit = self.POINTS_TO_EXIT

    def _compute_target_tile(self, pacman, all_ghosts):
        blinky = self.get_ghost(all_ghosts, Blinky)
        if not blinky:
            return pacman._get_grid_coordinates()
        
        brow, bcol = blinky._get_grid_coordinates()
        prow, pcol = pacman._get_grid_coordinates()
        
        if pacman._current_orientation == 1:    prow -= self.CHASE_OFFSET
        elif pacman._current_orientation == 2:  prow += self.CHASE_OFFSET
        elif pacman._current_orientation == 3:  pcol -= self.CHASE_OFFSET
        elif pacman._current_orientation == 4:  pcol += self.CHASE_OFFSET

        target_row = 2 * prow - brow
        target_col = 2 * pcol - bcol
        return (target_row, target_col)
    
    def _should_exit_house(self, pacman, all_ghosts) -> bool:
        return pacman.total_points >= self._points_required_to_exit
    
    def _initial_config (self) -> None:
        super()._initial_config()
        config = Settings.get("inky")
        self.INKY_SCATTER_TARGET = tuple(config.get("scatter_target"))
        self.POINTS_TO_EXIT = config.get("points_to_exit")
        self.CHASE_OFFSET = config.get("chase_offset")

class Clyde (Ghost):
    
    def __init__(self, x, y, environment):
        sprite_paths = {
            1: 'src/images/clyde_up.png',    
            2: 'src/images/clyde_down.png',  
            3: 'src/images/clyde_left.png',  
            4: 'src/images/clyde_right.png', 
        }
        
        super().__init__(x, y, environment, sprite_paths)
        
        self.SCATTER_TARGET_TILE = self.CLYDE_SCATTER_TARGET
        self._points_required_to_exit = self.POINTS_TO_EXIT

    def _compute_target_tile(self, pacman, all_ghosts):
        prow, pcol = pacman._get_grid_coordinates()
        grow, gcol = self._get_grid_coordinates()

        distance_sq = (prow - grow)**2 + (pcol - gcol)**2
        if distance_sq > self.DISTANCE_THRESHOLD_SQUARED: 
            return (prow, pcol)
        else: 
            return self.SCATTER_TARGET_TILE

    def _should_exit_house(self, pacman, all_ghosts) -> bool:
        return pacman.total_points >= self._points_required_to_exit
    
    def _initial_config (self) -> None:
        super()._initial_config()
        config = Settings.get("clyde")
        self.CLYDE_SCATTER_TARGET = tuple(config.get("scatter_target"))
        self.POINTS_TO_EXIT = config.get("points_to_exit")
        self.DISTANCE_THRESHOLD_SQUARED = config.get("distance_threshold_squared")