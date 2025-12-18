from src.entities.ghost import Ghost
from src.entities.blinky import Blinky

class Inky (Ghost):
    
    def __init__(self, x, y, environment, ghost_config: GhostConfig, inky_config: InkyConfig, teleport_config: TeleportConfig):
        sprite_paths = {
            1: 'src/data/images/inky_up.png',    
            2: 'src/data/images/inky_down.png',  
            3: 'src/data/images/inky_left.png',  
            4: 'src/data/images/inky_right.png', 
        }

        super().__init__(x, y, environment, sprite_paths, ghost_config, teleport_config)

        self.CHASE_OFFSET        = inky_config.CHASE_OFFSET
        self.INKY_SCATTER_TARGET = inky_config.INKY_SCATTER_TARGET
        self.POINTS_TO_EXIT      = inky_config.POINTS_TO_EXIT
        
        self.SCATTER_TARGET_TILE      = self.INKY_SCATTER_TARGET
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