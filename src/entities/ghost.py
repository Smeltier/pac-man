import random
import pygame

from abc import abstractmethod

from src.core.states                       import GhostState, GameState 
from src.entities.entity                   import Entity
from src.data.class_config.ghost_config    import GhostConfig
from src.data.class_config.teleport_config import TeleportConfig

class Ghost (Entity):
    
    OPPOSITE_ORIENTATION = {1: 2, 2: 1, 3: 4, 4: 3, 0: 0}

    def __init__(self, x, y, environment, sprite_paths: dict[int, str], ghost_config: GhostConfig, teleport_config: TeleportConfig):
        super().__init__(x, y, environment)

        self.NORMAL_SPEED = ghost_config.NORMAL_SPEED
        self.EATEN_SPEED = ghost_config.EATEN_SPEED
        self.HOUSE_RESPAWN_TIME_MS = ghost_config.HOUSE_RESPAWN_TIME_MS
        self.SCATTER_TARGET = ghost_config.SCATTER_TARGET
        self.HOUSE_EXIT_POSITION = ghost_config.HOUSE_EXIT_POSITION
        self.HOUSE_DOOR_POSITION = ghost_config.HOUSE_DOOR_POSITION
        self.HOUSE_WAIT_POSITION = ghost_config.HOUSE_WAIT_POSITION

        self.TELEPORT_MIN_X      = teleport_config.TELEPORT_MIN_X
        self.TELEPORT_MAX_X      = teleport_config.TELEPORT_MAX_X
        self.TELEPORT_WRAP_X_MIN = teleport_config.TELEPORT_WRAP_X_MIN
        self.TELEPORT_WRAP_X_MAX = teleport_config.TELEPORT_WRAP_X_MAX

        self._start_position = pygame.Vector2(x, y)
        self._current_speed = self.NORMAL_SPEED 
        self._current_orientation = 4 
        
        self._start_mode = GhostState.IN_HOUSE
        self._current_mode = GhostState.IN_HOUSE
        self._previous_mode = GhostState.IN_HOUSE
        self._last_game_state = GameState.CHASE
        self._is_immune = False 
        
        self._exit_timer_ms = 0 
        
        self._directional_sprites = self._load_directional_sprites(sprite_paths)
        self._vulnerable_sprites = self._load_vulnerable_sprites()
        self._eaten_sprites = self._load_eaten_sprites()
        
        self._vulnerable_animation_timer_ms = 0.0
        self._vulnerable_animation_frame_index = 0
        self._vulnerable_animation_speed_ms = 0.15 

    def update(self, delta_time):
        if self._ENVIRONMENT.game_state == GameState.GAME_OVER: 
            return

        pacman = self._ENVIRONMENT.entities[0] 
        all_ghosts = [entity for entity in self._ENVIRONMENT.entities if isinstance(entity, Ghost)]
        
        self._synchronize_immunity_with_game_state()
        
        self._previous_mode = self._current_mode
        self._update_ghost_behavior_state(pacman, all_ghosts)
        self._handle_direction_reversal_on_state_change()

        self._update_animation_frames(delta_time)

        if self._current_mode != GhostState.IN_HOUSE:
            self._process_movement_physics(pacman, all_ghosts)

    def draw(self, screen):
        x_position, y_position = int(self.position.x), int(self.position.y)
        current_sprite = None

        if self._current_mode == GhostState.VULNERABLE:
            current_sprite = self._vulnerable_sprites[self._vulnerable_animation_frame_index]
        elif self._current_mode == GhostState.EATEN:
            current_sprite = self._eaten_sprites.get(self._current_orientation)
        else:
            current_sprite = self._directional_sprites.get(self._current_orientation)

        if current_sprite: 
            rectangle = current_sprite.get_rect(center=(x_position, y_position))
            screen.blit(current_sprite, rectangle)

    def set_eaten(self):
        self._current_mode = GhostState.EATEN
        self._is_immune = True 

    def reset(self) -> None:
        self.position = self._start_position.copy()
        self._current_orientation = 4
        self._current_mode = self._start_mode
        self._current_speed = self.NORMAL_SPEED
        self._exit_timer_ms = 0
        self._is_immune = False

        if self._current_mode == GhostState.SCATTER:
            self._release_ghost_from_house()

    def get_collision_rectangle(self) -> pygame.Rect:
        collision_rectangle = pygame.Rect(0, 0, 32, 32)
        collision_rectangle.center = (int(self.position.x), int(self.position.y))
        return collision_rectangle

    def get_ghost(self, all_ghosts, ghost_class):
        return next((ghost for ghost in all_ghosts if isinstance(ghost, ghost_class)), None)

    @abstractmethod
    def _compute_target_tile(self, pacman, all_ghosts) -> tuple:
        raise NotImplementedError("A subclasse deve implementar _compute_target_tile")
    
    @abstractmethod
    def _should_exit_house(self, pacman, all_ghosts) -> bool:
        raise NotImplementedError("A subclasse deve implementar _should_exit_house")
    
    def _synchronize_immunity_with_game_state(self):
        current_game_state = self._ENVIRONMENT.game_state
        
        if (current_game_state == GameState.VULNERABLE and 
            self._last_game_state != GameState.VULNERABLE):
            self._is_immune = False
            
        self._last_game_state = current_game_state

    def _update_ghost_behavior_state(self, pacman, all_ghosts):
        game_mode = self._ENVIRONMENT.game_state

        if self._current_mode == GhostState.IN_HOUSE:
            if self._should_exit_house(pacman, all_ghosts):
                self._release_ghost_from_house()
            return 

        if self._current_mode == GhostState.EATEN:
            current_row, current_column = self._get_grid_coordinates()
            door_row, door_column = self.HOUSE_DOOR_POSITION
            
            if abs(current_row - door_row) < 1 and abs(current_column - door_column) < 1:
                self._enter_house_to_respawn()
            return

        if self._current_mode not in [GhostState.IN_HOUSE, GhostState.EXITING]:
            
            if game_mode == GameState.VULNERABLE:
                if self._current_mode != GhostState.EATEN and not self._is_immune:
                    self._current_mode = GhostState.VULNERABLE
                elif self._is_immune:
                     self._current_mode = self._ENVIRONMENT.get_global_ghost_mode()
            
            elif self._previous_mode == GhostState.VULNERABLE and game_mode != GameState.VULNERABLE:
                 self._current_mode = self._ENVIRONMENT.get_global_ghost_mode()
            
            elif game_mode == GameState.CHASE:
                 self._current_mode = self._ENVIRONMENT.get_global_ghost_mode()

    def _handle_direction_reversal_on_state_change(self):
        if self._current_mode != self._previous_mode:
            is_becoming_vulnerable = self._current_mode == GhostState.VULNERABLE
            was_vulnerable = self._previous_mode == GhostState.VULNERABLE
            
            valid_previous_state = self._previous_mode not in [GhostState.IN_HOUSE, GhostState.EATEN, GhostState.EXITING]

            if (is_becoming_vulnerable or was_vulnerable) and valid_previous_state:
                self._current_orientation = self.OPPOSITE_ORIENTATION[self._current_orientation]

    def _process_movement_physics(self, pacman, all_ghosts):
        if self._ENVIRONMENT.game_state == GameState.GAME_OVER: 
            return

        if self._align_to_grid_center():
            is_dead_end = not self._is_move_valid(self._current_orientation)
            is_intersection = self._is_intersection()

            if is_dead_end or is_intersection:
                self._current_orientation = self._calculate_best_direction(pacman, all_ghosts)

        self._apply_velocity()
        self._handle_teleport()

    def _calculate_best_direction(self, pacman, all_ghosts):
        current_row, current_column = self._get_grid_coordinates()
        valid_choices = []

        for direction in (1, 2, 3, 4):
            if self._is_move_valid(direction) and direction != self.OPPOSITE_ORIENTATION[self._current_orientation]:
                valid_choices.append(direction)
                
        if not valid_choices:
            if self._is_move_valid(self.OPPOSITE_ORIENTATION[self._current_orientation]):
                 return self.OPPOSITE_ORIENTATION[self._current_orientation]
            return 0 

        if self._current_mode == GhostState.VULNERABLE:
            return random.choice(valid_choices)

        target_tile = None

        if self._current_mode == GhostState.CHASE:
            target_tile = self._compute_target_tile(pacman, all_ghosts)
        elif self._current_mode == GhostState.SCATTER:
            target_tile = self.SCATTER_TARGET_TILE
        elif self._current_mode == GhostState.EATEN:
            target_tile = self.HOUSE_DOOR_POSITION

        if target_tile is None: 
            return random.choice(valid_choices)

        target_row, target_column = target_tile

        column_offset = {1: 0, 2: 0, 3: -1, 4: 1, 0: 0}
        row_offset = {1: -1, 2: 1, 3: 0, 4: 0, 0: 0}

        def distance_squared(direction):
            next_row = current_row + row_offset[direction]
            next_column = current_column + column_offset[direction]
            return (next_row - target_row) ** 2 + (next_column - target_column) ** 2

        return min(valid_choices, key=distance_squared)

    def _apply_velocity(self):
        if self._current_mode == GhostState.EATEN:
            self._current_speed = self.EATEN_SPEED
        elif self._current_mode == GhostState.VULNERABLE:
            self._current_speed = self.NORMAL_SPEED * 0.75
        else:
            self._current_speed = self.NORMAL_SPEED

        if self._current_orientation == 1: self.position.y -= self._current_speed
        elif self._current_orientation == 2: self.position.y += self._current_speed
        elif self._current_orientation == 3: self.position.x -= self._current_speed
        elif self._current_orientation == 4: self.position.x += self._current_speed

    def _align_to_grid_center(self):
        current_row, current_column = self._get_grid_coordinates()
        cell_width, cell_height = self._ENVIRONMENT.cell_width, self._ENVIRONMENT.cell_height
        
        center_x = current_column * cell_width + cell_width / 2
        center_y = current_row * cell_height + cell_height / 2

        if abs(self.position.x - center_x) < self._current_speed and abs(self.position.y - center_y) < self._current_speed:
            self.position.x = center_x
            self.position.y = center_y
            return True
            
        return False

    def _is_move_valid(self, direction):
        if direction == 0: 
            return True
        
        current_row, current_column = self._get_grid_coordinates()
        
        if direction == 1:   current_row -= 1 
        elif direction == 2: current_row += 1 
        elif direction == 3: current_column -= 1 
        elif direction == 4: current_column += 1 

        maze_matrix = self._ENVIRONMENT.matrix
        original_layout = self._ENVIRONMENT._maze.maze_layout 

        if current_row < 0 or current_column < 0 or current_row >= len(maze_matrix) or current_column >= len(maze_matrix[0]):
            return False

        if self._current_mode == GhostState.EATEN and original_layout[current_row][current_column] == 9:
            return True

        return maze_matrix[current_row][current_column] != -1

    def _is_intersection(self) -> bool:
        valid_directions_count = 0
        
        for direction in (1, 2, 3, 4):
            if direction != self.OPPOSITE_ORIENTATION[self._current_orientation] and self._is_move_valid(direction):
                valid_directions_count += 1
                
        return valid_directions_count > 1

    def _get_grid_coordinates(self):
        row = int(self.position.y // self._ENVIRONMENT.cell_height)
        col = int(self.position.x // self._ENVIRONMENT.cell_width)
        return row, col

    def _release_ghost_from_house(self):
        cell_width = self._ENVIRONMENT.cell_width
        cell_height = self._ENVIRONMENT.cell_height
        house_exit_row, house_exit_column = self.HOUSE_EXIT_POSITION
        
        self.position = pygame.Vector2(x = house_exit_column * cell_width + cell_width // 2, y = house_exit_row * cell_height + cell_height // 2)
        self._current_mode = self._ENVIRONMENT.get_global_ghost_mode()
        self._current_orientation = 1 
        self._exit_timer_ms = 0

    def _enter_house_to_respawn(self):
        self._current_mode = GhostState.IN_HOUSE
        self._current_speed = self.NORMAL_SPEED

        cell_width = self._ENVIRONMENT.cell_width
        cell_height = self._ENVIRONMENT.cell_height
        house_wait_row, house_wait_column = self.HOUSE_WAIT_POSITION

        self.position = pygame.Vector2(x = house_wait_column * cell_width + cell_width / 2, y = house_wait_row * cell_height + cell_height / 2)
        self._exit_timer_ms = pygame.time.get_ticks() + self.HOUSE_RESPAWN_TIME_MS

    def _update_animation_frames(self, delta_time):
        if self._current_mode == GhostState.VULNERABLE:
            self._vulnerable_animation_timer_ms += delta_time
            
            if self._vulnerable_animation_timer_ms >= self._vulnerable_animation_speed_ms:
                self._vulnerable_animation_timer_ms -= self._vulnerable_animation_speed_ms
                self._vulnerable_animation_frame_index = (self._vulnerable_animation_frame_index + 1) % len(self._vulnerable_sprites)
        
        elif self._current_mode in [GhostState.CHASE, GhostState.SCATTER]:
            pass 

    def _handle_teleport(self) -> None:
        if self.position.x <= self.TELEPORT_MIN_X: 
            self.position.x = self.TELEPORT_WRAP_X_MIN
        if self.position.x >= self.TELEPORT_MAX_X: 
            self.position.x = self.TELEPORT_WRAP_X_MAX

    def _load_directional_sprites(self, paths: dict[int, str]) -> dict[int, pygame.Surface]:
        sprites = {}

        for direction, path in paths.items():
            try:
                image = pygame.image.load(path)
                sprites[direction] = pygame.transform.scale(image, (40, 40))

            except pygame.error:
                sprites[direction] = pygame.Surface((40, 40), pygame.SRCALPHA)

        return sprites

    def _load_vulnerable_sprites(self) -> list[pygame.Surface]:
        vulnerable_sprites = []

        try:
            sprite_blue = pygame.image.load('src/data/images/vulnerable_sprite.png')
            sprite_white = pygame.image.load('src/data/images/vulnerable_sprite_white.png')
            vulnerable_sprites.append(pygame.transform.scale(sprite_blue, (40, 40)))
            vulnerable_sprites.append(pygame.transform.scale(sprite_white, (40, 40)))

        except pygame.error:
            empty = pygame.Surface((40, 40), pygame.SRCALPHA)
            vulnerable_sprites = [empty, empty]

        return vulnerable_sprites

    def _load_eaten_sprites(self) -> dict[int, pygame.Surface]:
        eaten_sprites = {}
        eaten_paths = {
            1: 'src/data/images/eyes_up.png',    
            2: 'src/data/images/eyes_down.png',  
            3: 'src/data/images/eyes_left.png',  
            4: 'src/data/images/eyes_right.png', 
        }

        for direction, path in eaten_paths.items():
            try:
                img = pygame.image.load(path)
                eaten_sprites[direction] = pygame.transform.scale(img, (40, 40))

            except pygame.error:
                eaten_sprites[direction] = pygame.Surface((40, 40), pygame.SRCALPHA)

        return eaten_sprites