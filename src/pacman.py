import pygame
from entity import Entity


class PacMan(Entity):

    def __init__(self, x, y, environment):
        super().__init__(x, y, environment)

        self._previous_orientation = 0
        self._current_orientation  = 0
        self._next_orientation     = 0
        self._animation_timer      = 0.0
        self._animation_speed      = 0.04
        self._animation_frame      = 0
        self._SPEED                = 2
        self.total_points          = 0
        self._SPRITES              = self._load_sprites()
        self._eat_sound            = pygame.mixer.Sound('src/sounds/Waka Waka.wav')
        self._eat_sound.set_volume(0.4)

    def _can_move(self, direction) -> bool:
        """ Verifica, baseado na próxima orientação, se o personagem pode se mover. """

        row, col = self._get_coordinates()

        if direction == 1:   row -= 1
        elif direction == 2: row += 1
        elif direction == 3: col -= 1
        elif direction == 4: col += 1
        elif direction == 0: return True

        if self._check_limits(row, col) and self._ENVIRONMENT.matrix[row][col] != -1:
            return True
        return False

    def _check_limits(self, row, col) -> bool:
        """ Verifica se o personagem está dentro dos limites da matriz. """

        matrix_height = len(self._ENVIRONMENT.matrix)
        matrix_width  = len(self._ENVIRONMENT.matrix[0])

        if not (0 <= row <= matrix_height and 0 <= col <= matrix_width):
            return False
        return True

    def _get_coordinates(self) -> tuple[int, int]:
        """ Converte a posição do personagem no ambiente para coordenadas na matriz. """

        row = int(self.position.y // self._ENVIRONMENT.cell_height)
        col = int(self.position.x // self._ENVIRONMENT.cell_width)
        return row, col

    def _handle_moviment(self) -> None:
        """ Lida com o movimento do personagem. """        

        if self._is_on_grid():
            self._play_eat_sound()
            self._update_score()

            if self._can_move(self._next_orientation):
                self._current_orientation = self._next_orientation
            elif not self._can_move(self._current_orientation):
                self._current_orientation = 0

        if self.position.x <= 15: 
            self.position.x = 880
        if self.position.x >= 885: 
            self.position.x = 20

        if self._current_orientation == 1:
            self.position.y -= self._SPEED
        elif self._current_orientation == 2:
            self.position.y += self._SPEED
        elif self._current_orientation == 3:
            self.position.x -= self._SPEED
        elif self._current_orientation == 4:
            self.position.x += self._SPEED

    def _is_on_grid(self) -> bool:
        """ Ajusta a posição do personagem no centro da célula. """

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
        """Carrega os sprites do personagem."""

        sprites = []
        for count in range(0, 3):
            image  = pygame.image.load(f'src/images/pacman_eat_{count}.png')
            sprite = pygame.transform.scale(image, (40, 40))
            sprites.append(sprite)
        return sprites

    def _play_eat_sound(self):
        """Toca um som quando o personagem come uma pastilha."""

        row, col = self._get_coordinates()

        if not self._check_limits(row, col):
            return

        point_type = self._ENVIRONMENT.matrix[row][col]
        if point_type in (1, 2) and self._current_orientation != 0:
            if self._eat_sound.get_num_channels() == 0:
                self._eat_sound.play(loops=-1)
        else:
            self._eat_sound.stop()


    def _update_orientation(self, keys) -> None:
        """Atualiza a próxima orientação do personagem baseado na tecla pressionada."""

        key_map = {
            pygame.K_UP    : 1,
            pygame.K_DOWN  : 2,
            pygame.K_LEFT  : 3,
            pygame.K_RIGHT : 4,
        }
        for key, orientation in key_map.items():
            if keys[key]:
                self._next_orientation = orientation

    def _update_score(self) -> None:
        """Aumenta a pontuação baseado em qual tipo de pastilha o personagem comeu."""

        row, col = self._get_coordinates()

        if not self._check_limits(row, col):
            return
        
        point_type = self._ENVIRONMENT.matrix[row][col]

        if point_type == 1:
            self._ENVIRONMENT.matrix[row][col] = 0
            self.total_points                  += 10
            self._ENVIRONMENT.total_tablets    -= 1
        elif point_type == 2:
            self._ENVIRONMENT.matrix[row][col] = 0
            self.total_points                  += 20
            self._ENVIRONMENT.total_tablets    -= 1
            self._ENVIRONMENT.set_vulnerable()

    def _update_sprite(self, delta_time) -> None:
        """Atualiza o sprite do personagem baseado no tempo."""

        if self._current_orientation == 0:
            self._current_orientation = self._previous_orientation
            return
        
        self._animation_timer += delta_time / 2

        if self._animation_timer >= self._animation_speed:
            self._animation_timer -= self._animation_speed
            self._animation_frame = (self._animation_frame + 1) % len(self._SPRITES)
        
        self._previous_orientation = self._current_orientation

    def draw(self, screen) -> None:
        """Desenha o personagem baseado na orientação atual."""

        x, y = int(self.position.x), int(self.position.y)
        sprite = self._SPRITES[self._animation_frame]
        angle = 0

        if self._current_orientation == 1:   angle = 90
        elif self._current_orientation == 2: angle = -90
        elif self._current_orientation == 3: angle = 180

        rotated_sprite = pygame.transform.rotate(surface=sprite, angle=angle)
        rectangle = rotated_sprite.get_rect(center=(x, y))
        screen.blit(rotated_sprite, rectangle)

    def update(self, delta_time) -> None:
        """Atualiza o personagem."""

        self._update_orientation(pygame.key.get_pressed())
        self._handle_moviment()
        self._update_sprite(delta_time)