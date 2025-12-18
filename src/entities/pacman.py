import pygame

from src.entities.entity import Entity
from src.core.states     import GhostState, GameState 

class PacMan (Entity):

    def __init__ (self, x: float, y: float, environment, config: dict, assets: dict) -> None:
        super().__init__(x, y, environment)

        self._speed = config.get("speed", 2)
        self._animation_speed_seconds = config.get("animation_speed_seconds", 0.04)
        self._collision_rect_size = config.get("collision_rect_size", 32)

        points_config = config.get("points", {})
        self._small_pellet_points = points_config.get("small_pellet", 10)
        self._power_pellet_points = points_config.get("power_pellet", 20)
        self._ghost_base_points = points_config.get("ghost_base", 100)

        teleport_config = config.get("teleport")
        self._teleport_min_x = teleport_config.get("min_x")
        self._teleport_max_x = teleport_config.get("max_x")
        self._teleport_wrap_x_min = teleport_config.get("wrap_x_min")
        self._teleport_wrap_x_max = teleport_config.get("wrap_x_max")

        self._start_position = pygame.Vector2(x, y)
        self._previous_orientation = 0
        self._current_orientation = 0
        self._next_orientation = 0
        self._animation_timer_s = 0.0
        self._animation_frame_index = 0
        self._total_points = 0
        self._ghosts_eaten_streak = 0
        self._sprites_move = assets.get("move")

    def update (self, delta_time: float) -> None:
        if self._environment.game_state != GameState.GAME_OVER:
            self._update_orientation(pygame.key.get_pressed())
            self._handle_movement()
            self._update_sprite(delta_time)
            self._check_collisions()

    def draw (self, screen) -> None:
        x, y = int(self.position.x), int(self.position.y)
        sprite = self._sprites[self._animation_frame_index]
        angle = 0

        if   self._current_orientation == 1: angle = 90
        elif self._current_orientation == 2: angle = -90
        elif self._current_orientation == 3: angle = 180
        
        rotated_sprite = pygame.transform.rotate(surface=sprite, angle=angle)
        rectangle = rotated_sprite.get_rect(center=(x, y))
        screen.blit(rotated_sprite, rectangle)

    def handle_death(self):
        self._environment.audio_manager.stop_waka()
        self._environment.handle_player_death()

    def reset(self) -> None:
        self.position = self._start_position.copy()
        self._current_orientation = 0
        self._next_orientation    = 0
        self._animation_frame_index = 0
        self._environment.audio_manager.stop_waka()
        self._ghosts_eaten_streak = 0
        
    def get_collision_rectangle (self) -> pygame.Rect:
        collision_rect = pygame.Rect(0, 0, self._collision_rect_size, self._collision_rect_size)
        collision_rect.center = (int(self.position.x), int(self.position.y))
        return collision_rect
    
    @property
    def total_points(self):
        return self._total_points
    
    def _can_move (self, direction) -> bool:
        row, col = self._get_grid_coordinates()

        if   direction == 1: row -= 1
        elif direction == 2: row += 1
        elif direction == 3: col -= 1
        elif direction == 4: col += 1
        elif direction == 0: return True

        if self._check_matrix_limits(row, col) and self._environment.matrix[row][col] != -1:
            return True

        return False

    def _check_matrix_limits (self, row, col) -> bool:
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

    def _handle_teleport(self) -> None:
        if self.position.x <= self._teleport_min_x: 
            self.position.x = self._teleport_wrap_x_min
        if self.position.x >= self._teleport_max_x: 
            self.position.x = self._teleport_wrap_x_max

    def _align_to_grid_center(self) -> bool:
        row, col = self._get_grid_coordinates()
        cell_width = self._ENVIRONMENT.cell_width
        cell_height = self._ENVIRONMENT.cell_height
        center_x = (col * cell_width) + (cell_width / 2)
        center_y = (row * cell_height) + (cell_height / 2)

        if abs(self.position.x - center_x) < self.SPEED and abs(self.position.y - center_y) < self.SPEED:
            self.position.x = center_x
            self.position.y = center_y
            return True

        return False

    def _load_sprites(self) -> list[pygame.Surface]:
        sprites = []
        for count in range(0, 3):
            try:
                image  = pygame.image.load(f'src/data/images/pacman_eat_{count}.png')
                sprite = pygame.transform.scale(image, (40, 40))
                sprites.append(sprite)

            except pygame.error as e:
                print(f"Erro: {e}")
                sprites.append(pygame.Surface((40, 40), pygame.SRCALPHA))
                
        return sprites

    def _play_eat_sound(self) -> None:
        row, col = self._get_grid_coordinates()
        if not self._check_matrix_limits(row, col):
            self._ENVIRONMENT.audio_manager.stop_waka()
            return

        point_type = self._ENVIRONMENT.matrix[row][col]

        if point_type in (1, 2) and self._current_orientation != 0:
            self._ENVIRONMENT.audio_manager.play_waka()

        else:
            self._ENVIRONMENT.audio_manager.stop_waka()

    def _update_orientation(self, keys) -> None:
        key_map = {pygame.K_UP: 1, pygame.K_DOWN: 2, pygame.K_LEFT: 3, pygame.K_RIGHT: 4}

        for key, orientation in key_map.items():
            if keys[key]: self._next_orientation = orientation

    def _update_score_and_map(self) -> None:
        row, col = self._get_grid_coordinates()
        if not self._check_matrix_limits(row, col):
            return
        
        point_type = self._ENVIRONMENT.matrix[row][col]

        if point_type in (1, 2):

            if point_type == 1:
                self._total_points += self.SMALL_PELLET_POINTS

            elif point_type == 2:
                self._total_points += self.POWER_PELLET_POINTS
                self._ENVIRONMENT.set_vulnerable()
                self._ghosts_eaten_streak = 0 

            self._ENVIRONMENT.matrix[row][col] = 0
            self._ENVIRONMENT.maze._total_tablets -= 1

            if self._ENVIRONMENT.maze.total_tablets <= 0:
                self._ENVIRONMENT.handle_victory()

    def _process_pellet_interaction(self):
        self._play_eat_sound() 
        self._update_score_and_map() 

    def _update_sprite(self, delta_time) -> None:
        if self._current_orientation == 0:
            self._current_orientation = self._previous_orientation
            self._animation_frame_index = 0 
            return

        self._animation_timer_s += delta_time / 2
        if self._animation_timer_s >= self.ANIMATION_SPEED_SECONDS:
            self._animation_timer_s -= self.ANIMATION_SPEED_SECONDS
            self._animation_frame_index = (self._animation_frame_index + 1) % len(self._sprites)

        self._previous_orientation = self._current_orientation

    def _check_collisions(self) -> None:
        from src.entities.ghost import Ghost
        
        pacman_rect = self.get_rect()
        
        all_ghosts = [entity for entity in self._ENVIRONMENT.entities if isinstance(entity, Ghost)]

        for ghost in all_ghosts:
            if pacman_rect.colliderect(ghost.get_collision_rectangle()):
                
                if ghost._current_mode == GhostState.VULNERABLE:
                    self._ghosts_eaten_streak += 1
                    points = self.GHOST_BASE_POINTS * (2 ** self._ghosts_eaten_streak)
                    self._total_points += points
                    ghost.set_eaten()
                
                elif ghost._current_mode in [GhostState.CHASE, GhostState.SCATTER]:
                    self.handle_death()