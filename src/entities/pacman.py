import pygame

from src.entities.entity import Entity
from src.states import GhostState, GameState 

class PacMan (Entity):

    def __init__ (self, x, y, environment) -> None:
        super().__init__(x, y, environment)

        self.start_position = pygame.Vector2(x, y)
        self._previous_orientation = 0
        self._current_orientation  = 0
        self._next_orientation     = 0
        self._animation_timer      = 0.0
        self._animation_speed      = 0.04
        self._animation_frame      = 0
        self._SPEED                = 2
        self.total_points          = 0
        self._ghosts_eaten_streak  = 0 
        self._SPRITES              = self._load_sprites()

    def _can_move (self, direction) -> bool:
        row, col = self._get_coordinates()

        if   direction == 1: row -= 1
        elif direction == 2: row += 1
        elif direction == 3: col -= 1
        elif direction == 4: col += 1
        elif direction == 0: return True

        if self._check_limits(row, col) and self._ENVIRONMENT.matrix[row][col] != -1:
            return True

        return False

    def _check_limits (self, row, col) -> bool:
        matrix_height = len(self._ENVIRONMENT.matrix)
        matrix_width  = len(self._ENVIRONMENT.matrix[0])
        return (0 <= row < matrix_height) and (0 <= col < matrix_width)

    def _get_coordinates(self) -> tuple[int, int]:
        row = int(self.position.y // self._ENVIRONMENT.cell_height)
        col = int(self.position.x // self._ENVIRONMENT.cell_width)
        return row, col

    def get_rect(self) -> pygame.Rect:
        collision_rect = pygame.Rect(0, 0, 32, 32)
        collision_rect.center = (int(self.position.x), int(self.position.y))
        return collision_rect

    def _handle_moviment(self) -> None:
        if self._is_on_grid():
            self._play_eat_sound() 
            self._update_score() 

            if self._can_move(self._next_orientation):
                self._current_orientation = self._next_orientation

            elif not self._can_move(self._current_orientation):
                self._current_orientation = 0
        
        if   self._current_orientation == 1: self.position.y -= self._SPEED
        elif self._current_orientation == 2: self.position.y += self._SPEED
        elif self._current_orientation == 3: self.position.x -= self._SPEED
        elif self._current_orientation == 4: self.position.x += self._SPEED

        self._handle_teleport()

    def _handle_teleport(self) -> None:
        if self.position.x <= 15: self.position.x = 880
        if self.position.x >= 885: self.position.x = 20

    def _is_on_grid(self) -> bool:
        row, col = self._get_coordinates()
        cell_width = self._ENVIRONMENT.cell_width
        cell_height = self._ENVIRONMENT.cell_height
        center_x = (col * cell_width) + (cell_width / 2)
        center_y = (row * cell_height) + (cell_height / 2)

        if abs(self.position.x - center_x) < self._SPEED and abs(self.position.y - center_y) < self._SPEED:
            self.position.x = center_x
            self.position.y = center_y
            return True

        return False

    def _load_sprites(self) -> list[pygame.Surface]:
        sprites = []
        for count in range(0, 3):
            try:
                image  = pygame.image.load(f'src/images/pacman_eat_{count}.png')
                sprite = pygame.transform.scale(image, (40, 40))
                sprites.append(sprite)

            except pygame.error as e:
                print(f"Erro: {e}")
                sprites.append(pygame.Surface((40, 40), pygame.SRCALPHA))
                
        return sprites

    def _play_eat_sound(self):
        row, col = self._get_coordinates()
        if not self._check_limits(row, col):
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

    def _update_score(self) -> None:
        row, col = self._get_coordinates()
        if not self._check_limits(row, col):
            return
        
        point_type = self._ENVIRONMENT.matrix[row][col]

        if point_type in (1, 2):

            if point_type == 1:
                self.total_points += 10

            elif point_type == 2:
                self.total_points += 20
                self._ENVIRONMENT.set_vulnerable()
                self._ghosts_eaten_streak = 0 

            self._ENVIRONMENT.matrix[row][col] = 0
            self._ENVIRONMENT.maze.total_tablets -= 1

            if self._ENVIRONMENT.maze.total_tablets <= 0:
                self._ENVIRONMENT.handle_victory()

    def _update_sprite(self, delta_time) -> None:
        if self._current_orientation == 0:
            self._current_orientation = self._previous_orientation
            self._animation_frame = 0 
            return

        self._animation_timer += delta_time / 2
        if self._animation_timer >= self._animation_speed:
            self._animation_timer -= self._animation_speed
            self._animation_frame = (self._animation_frame + 1) % len(self._SPRITES)

        self._previous_orientation = self._current_orientation

    def draw(self, screen) -> None:
        x, y = int(self.position.x), int(self.position.y)
        sprite = self._SPRITES[self._animation_frame]
        angle = 0

        if   self._current_orientation == 1: angle = 90
        elif self._current_orientation == 2: angle = -90
        elif self._current_orientation == 3: angle = 180
        
        rotated_sprite = pygame.transform.rotate(surface=sprite, angle=angle)
        rectangle = rotated_sprite.get_rect(center=(x, y))
        screen.blit(rotated_sprite, rectangle)

    def _check_collisions(self):
        """ Verifica colisões com todos os fantasmas. """
        from src.entities.ghost import Ghost
        
        pacman_rect = self.get_rect()
        
        all_ghosts = [e for e in self._ENVIRONMENT.entities if isinstance(e, Ghost)]

        for ghost in all_ghosts:
            if pacman_rect.colliderect(ghost.get_rect()):
                
                if ghost.mode == GhostState.VULNERABLE:
                    self._ghosts_eaten_streak += 1
                    points = 100 * (2 ** self._ghosts_eaten_streak)
                    self.total_points += points
                    ghost.set_eaten()
                
                elif ghost.mode in [GhostState.CHASE, GhostState.SCATTER]:
                    self.handle_death()

    def handle_death(self):
        """ Lida com a morte do Pac-Man. """
        
        self._ENVIRONMENT.audio_manager.stop_waka()
        self._ENVIRONMENT.handle_player_death()

    def update(self, delta_time) -> None:
        """Atualiza o personagem."""
        
        if self._ENVIRONMENT.game_state != GameState.GAME_OVER:
            self._update_orientation(pygame.key.get_pressed())
            self._handle_moviment()
            self._update_sprite(delta_time)
            self._check_collisions()

    def reset(self):
        self.position = self.start_position.copy()
        self._current_orientation = 0
        self._next_orientation    = 0
        self._animation_frame = 0
        self._ENVIRONMENT.audio_manager.stop_waka()