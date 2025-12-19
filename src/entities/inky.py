from src.entities.ghost import Ghost
from src.entities.blinky import Blinky

class Inky (Ghost):
    
    def __init__(self, x, y, environment, config: dict, assets: dict):
        super().__init__(x, y, environment, config, assets)

        inky_config: dict = config.get("inky", {})
        self._chase_offset = inky_config.get("chase_offset", 0)
        self._scatter_target_tile = inky_config.get("scatter_target", (0, 0))
        self._points_required_to_exit = inky_config.get("points_to_exit", 0)

    def _compute_target_tile(self, pacman, all_ghosts) -> tuple[int, int]:
        blinky = self.get_ghost(all_ghosts, Blinky)
        if not blinky:
            return pacman._get_grid_coordinates()
        
        brow, bcol = blinky._get_grid_coordinates()
        prow, pcol = pacman._get_grid_coordinates()
        
        if pacman._current_orientation == 1:    prow -= self._chase_offset
        elif pacman._current_orientation == 2:  prow += self._chase_offset
        elif pacman._current_orientation == 3:  pcol -= self._chase_offset
        elif pacman._current_orientation == 4:  pcol += self._chase_offset

        target_row = 2 * prow - brow
        target_col = 2 * pcol - bcol
        return (target_row, target_col)
    
    def _should_exit_house(self, pacman, all_ghosts) -> bool:
        return pacman.total_points >= self._points_required_to_exit