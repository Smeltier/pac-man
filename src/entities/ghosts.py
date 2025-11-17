import pygame

from src.entities.ghost import Ghost, GhostState

class Blinky (Ghost):
    """ Fantasma vermelho (Blinky). Mira diretamente na posição do Pac-Man. """

    def __init__(self, x, y, environment):
        super().__init__(x, y, environment, 'src/images/ghost_0.png')
        self.scatter_target = (2, 27)
        self.mode = GhostState.SCATTER
        self._release_ghost()

    def _compute_target(self, pacman, all_ghosts):
        return pacman._get_coordinates()
    
    def _should_exit_house(self, pacman, all_ghosts) -> bool:
        return False

class Pinky (Ghost):
    """ Fantasma rosa (Pinky). Mira 4 casas à frente da direção atual do Pac-Man. """

    def __init__(self, x, y, environment):
        super().__init__(x, y, environment, 'src/images/ghost_1.png')
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
    """ Fantasma ciano (Inky). Usa um vetor do Blinky até 2 casas à frente do Pac-Man. """

    def __init__(self, x, y, environment):
        super().__init__(x, y, environment, 'src/images/ghost_2.png')
        self.scatter_target = (34, 27)
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
    """ Fantasma laranja (Clyde). Persegue o Pac-Man, mas foge se chegar perto. """

    def __init__(self, x, y, environment):
        super().__init__(x, y, environment, 'src/images/ghost_3.png')
        self.scatter_target = (34, 2)
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