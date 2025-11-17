import pygame
import random

from abc import abstractmethod
from enum import Enum, auto

from src.entities.entity import Entity

class Ghost (Entity):

    def __init__(self, x, y, environment, sprite_path):
        super().__init__(x, y, environment)
        
        self.speed = 2
        self.current_orientation: int = 4
        self.next_orientation = 4
        self._orientations = (1, 2, 3, 4)
        self._opposite_orientation = {1:2, 2:1, 3:4, 4:3}

        self.in_house = True
        self.mode = GhostState.IN_HOUSE
        self.previous_mode = GhostState.IN_HOUSE

        self.scatter_target = (0, 0)
        self._house_exit_position = (15, 12)

        self._exit_timer = 0
        self._sprite_path = sprite_path 
        self._sprite = self._load_sprite()

    @abstractmethod
    def _compute_target(self, pacman, all_ghosts):
        """ Calcula a posição-alvo da caçada. """
        raise NotImplementedError("A subclasse deve implementar _compute_target")
    
    @abstractmethod
    def _should_exit_house(self, pacman, all_ghosts) -> bool:
        """ Verifica se o fantasma deve sair da casa. """
        raise NotImplementedError("A subclasse deve implementar _should_exit_house")


    def _load_sprite(self):
        image = pygame.image.load(self._sprite_path)
        return pygame.transform.scale(image, (40, 40))

    def _get_coordinates(self):
        row = int(self.position.y // self._ENVIRONMENT.cell_height)
        col = int(self.position.x // self._ENVIRONMENT.cell_width)
        return row, col
    
    def _is_intersection(self) -> bool:
        valid_directions = 0
        for direction in self._orientations:
            if direction != self._opposite_orientation[self.current_orientation] and self._can_move(direction):
                valid_directions += 1

        return valid_directions > 1

    def _is_on_grid(self):
        row, col = self._get_coordinates()
        cw, ch = self._ENVIRONMENT.cell_width, self._ENVIRONMENT.cell_height

        cx = col * cw + cw / 2
        cy = row * ch + ch / 2

        if abs(self.position.x - cx) < self.speed and abs(self.position.y - cy) < self.speed:
            self.position.x = cx
            self.position.y = cy

            return True
        return False

    def _can_move(self, direction):
        if direction == 0:
            return True
        row, col = self._get_coordinates()

        if direction == 1:   row -= 1
        elif direction == 2: row += 1
        elif direction == 3: col -= 1
        elif direction == 4: col += 1

        m = self._ENVIRONMENT.matrix
        if row < 0 or col < 0 or row >= len(m) or col >= len(m[0]):
            return False
        
        return m[row][col] != -1


    def _choose_direction(self, pacman, all_ghosts) -> int:
        row, col = self._get_coordinates()

        valid_choices = []
        for direction in self._orientations:
            if self._can_move(direction) and direction != self._opposite_orientation[self.current_orientation]:
                valid_choices.append(direction)

        if not valid_choices:
            if self._can_move(self._opposite_orientation.get(self.current_orientation)):
                return self._opposite_orientation.get(self.current_orientation) # type: ignore
            return 0
        
        if self.mode == GhostState.VULNERABLE:
            return random.choice(valid_choices)
        
        target_tile = None

        if self.mode == GhostState.CHASE:
            target_tile = self._compute_target(pacman, all_ghosts)
        elif self.mode == GhostState.SCATTER:
            target_tile = self.scatter_target
        elif self.mode == GhostState.EATEN:
            target_tile = self._house_exit_position

        if target_tile is None:
            return random.choice(valid_choices)
        
        target_row, target_col = target_tile

        def dist_sq(d):
            dx = {1: 0, 2: 0, 3: -1, 4: 1, 0: 0}
            dy = {1: -1, 2: 1, 3: 0, 4: 0, 0: 0}
            nr = row + dy[d]
            nc = col + dx[d]

            return (nr - target_row) ** 2 + (nc - target_col) ** 2
        
        min_distance = float('inf')
        best_direction = 0

        priority_order = [1, 3, 2, 4]

        for d in priority_order:
            if d in valid_choices:
                d_sq = dist_sq(d)
                if d_sq < min_distance:
                    min_distance = d_sq
                    best_direction = d

        return best_direction

    def _move(self):
        if self.current_orientation == 1:
            self.position.y -= self.speed
        elif self.current_orientation == 2:
            self.position.y += self.speed
        elif self.current_orientation == 3:
            self.position.x -= self.speed
        elif self.current_orientation == 4:
            self.position.x += self.speed

    def _handle_moviment(self, pacman, all_ghosts):
        if self._is_on_grid():
            if not self._can_move(self.current_orientation) or self._is_intersection():
                self.current_orientation = self._choose_direction(pacman, all_ghosts)
        self._move()

    def _release_ghost(self):
        cw = self._ENVIRONMENT.cell_width
        ch = self._ENVIRONMENT.cell_height
        hr, hc = self._house_exit_position

        self.position = pygame.Vector2(
            x = hc * cw + cw // 2,
            y = hr * ch + ch // 2,
        )

        self.mode = GhostState.SCATTER
        self.current_orientation = 1

    def update(self, dt):
        pacman = self._ENVIRONMENT.entities[0]
        all_ghosts = [ e for e in self._ENVIRONMENT.entities if isinstance(e, Ghost) ]

        self.previous_mode = self.mode

        if self.mode == GhostState.IN_HOUSE:
            if self._should_exit_house(pacman, all_ghosts):
                self._release_ghost()

        elif self.mode == GhostState.EATEN:
            row, col = self._get_coordinates()
            hr, hc = self._house_exit_position
            if abs(row - hr) < 1 and abs(col - hc) < 1:
                self.mode = GhostState.IN_HOUSE
        
        elif self.mode not in [GhostState.IN_HOUSE]:
            if self._ENVIRONMENT.game_state == "vulnerable":
                self.mode = GhostState.VULNERABLE
            
            elif self.previous_mode == GhostState.VULNERABLE and self._ENVIRONMENT.game_state != "vulnerable":
                 self.mode = self._ENVIRONMENT.get_global_ghost_mode() 
            
            else:
                 self.mode = self._ENVIRONMENT.get_global_ghost_mode()

        if self.mode != self.previous_mode:
            if self.mode == GhostState.VULNERABLE or self.previous_mode == GhostState.VULNERABLE:
                if self.previous_mode not in [GhostState.IN_HOUSE, GhostState.EATEN]:
                    self.current_orientation = self._opposite_orientation[self.current_orientation]

        if self.mode != GhostState.IN_HOUSE:
            self._handle_moviment(pacman, all_ghosts)

    def draw(self, screen):
        x, y = int(self.position.x), int(self.position.y)
        rectangle = self._sprite.get_rect(center=(x, y))
        screen.blit(self._sprite, rectangle)

    def get_ghost(self, all_ghosts, cls):
        return next((g for g in all_ghosts if isinstance(g, cls)), None)
    
class GhostState (Enum):
    IN_HOUSE = auto()
    CHASE = auto()
    SCATTER = auto()
    VULNERABLE = auto()
    EATEN = auto()