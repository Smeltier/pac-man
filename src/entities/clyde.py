from src.entities.ghost import Ghost
from src.data.class_config.clyde_config import ClydeConfig
from src.data.class_config.ghost_config import GhostConfig
from src.data.class_config.teleport_config import TeleportConfig

class Clyde (Ghost):
    
    def __init__(self, x, y, environment, ghost_config: GhostConfig, clyde_config: ClydeConfig, teleport_config: TeleportConfig):
        sprite_paths = {
            1: 'src/data/images/clyde_up.png',    
            2: 'src/data/images/clyde_down.png',  
            3: 'src/data/images/clyde_left.png',  
            4: 'src/data/images/clyde_right.png', 
        }
        
        super().__init__(x, y, environment, sprite_paths, ghost_config, teleport_config)

        self.CLYDE_SCATTER_TARGET       = clyde_config.CLYDE_SCATTER_TARGET
        self.DISTANCE_THRESHOLD_SQUARED = clyde_config.DISTANCE_THRESHOLD_SQUARED
        self.POINTS_TO_EXIT             = clyde_config.POINTS_TO_EXIT
        
        self.SCATTER_TARGET_TILE      = self.CLYDE_SCATTER_TARGET
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