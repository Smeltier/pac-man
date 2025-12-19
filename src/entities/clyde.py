from src.entities.ghost import Ghost

class Clyde (Ghost):
    
    def __init__(self, x, y, environment, config: dict, assets: dict):
        super().__init__(x, y, environment, config, assets)

        clyde_config: dict = config.get("clyde", {})
        self._scatter_target_tile = clyde_config.get("scatter_target", (0, 0))
        self._points_required_to_exit = clyde_config.get("points_to_exit", 0)
        self._distance_threshold_squared = clyde_config.get("distance_threshold_squared", 0)

    def _compute_target_tile(self, pacman, all_ghosts) -> tuple[int, int]:
        prow, pcol = pacman._get_grid_coordinates()
        grow, gcol = self._get_grid_coordinates()

        distance_sq = (prow - grow)**2 + (pcol - gcol)**2
        if distance_sq > self._distance_threshold_squared: 
            return (prow, pcol)
        
        else: return self._scatter_target_tile

    def _should_exit_house(self, pacman, all_ghosts) -> bool:
        return pacman.total_points >= self._points_required_to_exit