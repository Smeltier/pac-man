from typing import TYPE_CHECKING

import pygame

from src.entities.entity import Entity
from src.core.states import GhostState, GameState 

if TYPE_CHECKING:
    from src.core.environment import Environment

class PacMan(Entity):

    _speed: float
    _animation_speed_seconds: float
    _small_pellet_points: int
    _power_pellet_points: int
    _ghost_base_points: int
    _previous_orientation: int
    _current_orientation: int
    _next_orientation: int
    _animation_timer_s: float
    _animation_frame_index: int
    _total_points: int
    _ghosts_eaten_streak: int
    _sprites_move: list[pygame.Surface]

    def __init__(self, x: float, y: float, environment: "Environment", config: dict, assets: dict) -> None:
        super().__init__(x, y, environment, config)

        self._speed = config.get("speed", 2)
        self._animation_speed_seconds = config.get("animation_speed_seconds", 0.02)

        points_config: dict = config.get("points", {})
        self._small_pellet_points = points_config.get("small_pellet", 10)
        self._power_pellet_points = points_config.get("power_pellet", 20)
        self._ghost_base_points = points_config.get("ghost_base", 100)

        self._sprites_move = assets.get("move", [])

        self._previous_orientation = 0
        self._current_orientation = 0
        self._next_orientation = 0
        self._animation_timer_s = 0.0
        self._animation_frame_index = 0
        self._total_points = 0
        self._ghosts_eaten_streak = 0

    def update(self, delta_time: float) -> None:
        if self._environment.game_state != GameState.GAME_OVER:
            self._update_orientation(pygame.key.get_pressed())
            self._handle_movement()
            self._update_sprite(delta_time)
            self._check_collisions()

    def draw(self, screen: pygame.Surface) -> None:
        x, y = int(self.position.x), int(self.position.y)
        sprite = self._sprites_move[self._animation_frame_index]
        angle = 0

        if   self._current_orientation == 1: angle = 90
        elif self._current_orientation == 2: angle = -90
        elif self._current_orientation == 3: angle = 180
        
        rotated_sprite = pygame.transform.rotate(surface=sprite, angle=angle)
        rectangle = rotated_sprite.get_rect(center=(x, y))
        screen.blit(rotated_sprite, rectangle)

    def reset(self) -> None:
        self.position = self._start_position.copy()
        self._current_orientation = 0
        self._next_orientation    = 0
        self._animation_frame_index = 0
        self._environment.audio_manager.stop_waka()
        self._ghosts_eaten_streak = 0

    def handle_death(self):
        self._environment.audio_manager.stop_waka()
        self._environment.handle_player_death()
        
    def get_collision_rectangle (self) -> pygame.Rect:
        collision_rect = pygame.Rect(0, 0, self._collision_rect_size, self._collision_rect_size)
        collision_rect.center = (int(self.position.x), int(self.position.y))
        return collision_rect
    
    @property
    def total_points(self):
        return self._total_points
    
    def _can_move(self, direction) -> bool:
        row, col = self._get_grid_coordinates()

        if   direction == 1: row -= 1
        elif direction == 2: row += 1
        elif direction == 3: col -= 1
        elif direction == 4: col += 1
        elif direction == 0: return True

        if self._check_matrix_limits(row, col) and self._environment.matrix[row][col] != -1:
            return True

        return False

    def _check_matrix_limits(self, row: int, col: int) -> bool:
        matrix_height = len(self._environment.matrix)
        matrix_width  = len(self._environment.matrix[0])
        return (0 <= row < matrix_height) and (0 <= col < matrix_width)

    def _get_grid_coordinates(self) -> tuple[int, int]:
        row = int(self.position.y // self._environment.cell_height)
        col = int(self.position.x // self._environment.cell_width)
        return row, col

    def _handle_movement(self) -> None:
        if self._align_to_grid_center():
            self._process_pellet_interaction() 

            if self._can_move(self._next_orientation):
                self._current_orientation = self._next_orientation

            elif not self._can_move(self._current_orientation):
                self._current_orientation = 0
        
        if   self._current_orientation == 1: self.position.y -= self._speed
        elif self._current_orientation == 2: self.position.y += self._speed
        elif self._current_orientation == 3: self.position.x -= self._speed
        elif self._current_orientation == 4: self.position.x += self._speed

        self._handle_teleport()

    def _align_to_grid_center(self) -> bool:
        row, col = self._get_grid_coordinates()
        cell_width = self._environment.cell_width
        cell_height = self._environment.cell_height
        center_x = (col * cell_width) + (cell_width / 2)
        center_y = (row * cell_height) + (cell_height / 2)

        if abs(self.position.x - center_x) < self._speed and abs(self.position.y - center_y) < self._speed:
            self.position.x = center_x
            self.position.y = center_y
            return True

        return False

    def _play_eat_sound(self) -> None:
        row, col = self._get_grid_coordinates()
        if not self._check_matrix_limits(row, col):
            self._environment.audio_manager.stop_waka()
            return

        point_type = self._environment.matrix[row][col]

        if point_type in (1, 2) and self._current_orientation != 0:
            self._environment.audio_manager.play_waka()

        else:
            self._environment.audio_manager.stop_waka()

    def _update_orientation(self, keys) -> None:
        key_map = {pygame.K_UP: 1, pygame.K_DOWN: 2, pygame.K_LEFT: 3, pygame.K_RIGHT: 4}

        for key, orientation in key_map.items():
            if keys[key]: self._next_orientation = orientation

    def _update_score_and_map(self) -> None:
        row, col = self._get_grid_coordinates()
        if not self._check_matrix_limits(row, col):
            return
        
        point_type = self._environment.matrix[row][col]

        if point_type in (1, 2):

            if point_type == 1:
                self._total_points += self._small_pellet_points

            elif point_type == 2:
                self._total_points += self._power_pellet_points
                self._environment.set_vulnerable()
                self._ghosts_eaten_streak = 0 

            self._environment.matrix[row][col] = 0
            self._environment.maze._total_tablets -= 1

            if self._environment.maze.total_tablets <= 0:
                self._environment.handle_victory()

    def _process_pellet_interaction(self):
        self._play_eat_sound() 
        self._update_score_and_map() 

    def _update_sprite(self, delta_time: float) -> None:
        if self._current_orientation == 0:
            self._current_orientation = self._previous_orientation
            self._animation_frame_index = 0 
            return

        self._animation_timer_s += delta_time / 2
        if self._animation_timer_s >= self._animation_speed_seconds:
            self._animation_timer_s -= self._animation_speed_seconds
            self._animation_frame_index = (self._animation_frame_index + 1) % len(self._sprites_move)

        self._previous_orientation = self._current_orientation

    def _check_collisions(self) -> None:
        from src.entities.ghost import Ghost
        
        pacman_rect = self.get_collision_rectangle()
        
        all_ghosts = [entity for entity in self._environment.entities if isinstance(entity, Ghost)]

        for ghost in all_ghosts:
            if pacman_rect.colliderect(ghost.get_collision_rectangle()):
                
                if ghost._current_mode == GhostState.VULNERABLE:
                    self._ghosts_eaten_streak += 1
                    points = self._ghost_base_points * (2 ** self._ghosts_eaten_streak)
                    self._total_points += points
                    ghost.set_eaten()
                
                elif ghost._current_mode in [GhostState.CHASE, GhostState.SCATTER]:
                    self.handle_death()