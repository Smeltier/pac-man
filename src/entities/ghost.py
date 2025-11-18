import pygame
import random
import math
from abc import abstractmethod

from src.entities.entity import Entity
from src.states import GhostState, GameState 

class Ghost (Entity):

    def __init__(self, x, y, environment, sprite_paths: dict[int, str]):
        super().__init__(x, y, environment)
        
        self.start_pos = pygame.Vector2(x, y)
        self.start_mode = GhostState.IN_HOUSE
        
        self.NORMAL_SPEED = 2
        self.EATEN_SPEED = 6 
        self.SPEED = self.NORMAL_SPEED 
        
        self.current_orientation = 4 
        self.opposite_orientation = {1: 2, 2: 1, 3: 4, 4: 3, 0: 0}
        
        self.mode = GhostState.IN_HOUSE
        self.previous_mode = GhostState.IN_HOUSE
        
        self.scatter_target = (0, 0)
        self.house_exit_pos = (12, 14)  
        self.house_door_pos = (13, 14) 
        self.house_wait_pos = (14, 14) 
        self.house_respawn_time = 3000 
        
        self._exit_timer = 0 
        
        self.immune = False 
        self.last_game_state = GameState.CHASE
        
        self._sprites = self._load_directional_sprites(sprite_paths)
        self._vulnerable_sprites = self._load_vulnerable_sprites()
        self._eaten_sprites = self._load_eaten_sprites()
        
        self._vulnerable_animation_timer = 0.0
        self._vulnerable_animation_frame = 0
        self._vulnerable_animation_speed = 0.15 

    @abstractmethod
    def _compute_target(self, pacman, all_ghosts) -> tuple:
        raise NotImplementedError("A subclasse deve implementar _compute_target")
    
    @abstractmethod
    def _should_exit_house(self, pacman, all_ghosts) -> bool:
        raise NotImplementedError("A subclasse deve implementar _should_exit_house")
    
    def _load_directional_sprites(self, paths: dict[int, str]) -> dict[int, pygame.Surface]:
        sprites = {}
        for direction, path in paths.items():
            try:
                image = pygame.image.load(path)
                sprites[direction] = pygame.transform.scale(image, (40, 40))
            except pygame.error as e:
                print(f"Erro ao carregar sprite direcional para {path} (Direção {direction}): {e}")
                sprites[direction] = pygame.Surface((40, 40), pygame.SRCALPHA)
        return sprites

    def _load_vulnerable_sprites(self) -> list[pygame.Surface]:
        vulnerable_sprites = []

        try:
            sprite1 = pygame.image.load('src/images/vulnerable_sprite.png')
            sprite2 = pygame.image.load('src/images/vulnerable_sprite_white.png')
            vulnerable_sprites.append(pygame.transform.scale(sprite1, (40, 40)))
            vulnerable_sprites.append(pygame.transform.scale(sprite2, (40, 40)))

        except pygame.error as e:
            print(f"Erro ao carregar sprites vulneráveis: {e}")
            empty_sprite = pygame.Surface((40, 40), pygame.SRCALPHA)
            vulnerable_sprites.append(empty_sprite)
            vulnerable_sprites.append(empty_sprite)

        return vulnerable_sprites

    def _load_eaten_sprites(self) -> dict[int, pygame.Surface]:
        eaten_sprites = {}
        eaten_paths = {
            1: 'src/images/eyes_up.png',    
            2: 'src/images/eyes_down.png',  
            3: 'src/images/eyes_left.png',  
            4: 'src/images/eyes_right.png', 
        }

        for direction, path in eaten_paths.items():

            try:
                image = pygame.image.load(path)
                eaten_sprites[direction] = pygame.transform.scale(image, (40, 40))

            except pygame.error as e:
                print(f"Erro ao carregar sprite de fantasma comido para {path} (Direção {direction}): {e}")
                eaten_sprites[direction] = pygame.Surface((40, 40), pygame.SRCALPHA)

        return eaten_sprites

    def _get_coordinates(self):
        row = int(self.position.y // self._ENVIRONMENT.cell_height)
        col = int(self.position.x // self._ENVIRONMENT.cell_width)
        return row, col

    
    def _is_intersection(self) -> bool:
        valid_directions = 0
        for d in (1, 2, 3, 4):
            if d != self.opposite_orientation[self.current_orientation] and self._can_move(d):
                valid_directions += 1
        return valid_directions > 1

    def _is_on_grid(self):
        row, col = self._get_coordinates()
        cw, ch = self._ENVIRONMENT.cell_width, self._ENVIRONMENT.cell_height
        cx = col * cw + cw / 2
        cy = row * ch + ch / 2

        if abs(self.position.x - cx) < self.SPEED and abs(self.position.y - cy) < self.SPEED:
            self.position.x = cx
            self.position.y = cy
            return True
            
        return False

    def _can_move(self, direction):
        if direction == 0: return True
        row, col = self._get_coordinates()
        if direction == 1:   row -= 1
        elif direction == 2: row += 1
        elif direction == 3: col -= 1
        elif direction == 4: col += 1

        m = self._ENVIRONMENT.matrix
        original_layout = self._ENVIRONMENT.maze.maze_layout 

        if row < 0 or col < 0 or row >= len(m) or col >= len(m[0]):
            return False

        if self.mode == GhostState.EATEN and original_layout[row][col] == 9:
            return True

        return m[row][col] != -1

    def _choose_direction(self, pacman, all_ghosts):
        row, col = self._get_coordinates()
        valid_choices = []

        for d in (1, 2, 3, 4):
            if self._can_move(d) and d != self.opposite_orientation[self.current_orientation]:
                valid_choices.append(d)
                
        if not valid_choices:
            if self._can_move(self.opposite_orientation[self.current_orientation]):
                 return self.opposite_orientation[self.current_orientation]
            return 0 

        if self.mode == GhostState.VULNERABLE:
            return random.choice(valid_choices)

        target_tile = None

        if self.mode == GhostState.CHASE:
            target_tile = self._compute_target(pacman, all_ghosts)
        elif self.mode == GhostState.SCATTER:
            target_tile = self.scatter_target
        elif self.mode == GhostState.EATEN:
            target_tile = self.house_door_pos

        if target_tile is None: return random.choice(valid_choices)

        tr, tc = target_tile

        dx = {1: 0, 2: 0, 3: -1, 4: 1, 0: 0}
        dy = {1: -1, 2: 1, 3: 0, 4: 0, 0: 0}

        def dist_sq(d):
            nr = row + dy[d]
            nc = col + dx[d]
            return (nr - tr) ** 2 + (nc - tc) ** 2

        return min(valid_choices, key=dist_sq)

    def _move(self):
        if self.mode == GhostState.EATEN:
            self.SPEED = self.EATEN_SPEED
        elif self.mode == GhostState.VULNERABLE:
            self.SPEED = self.NORMAL_SPEED * 0.75
        else:
            self.SPEED = self.NORMAL_SPEED

        if self.current_orientation == 1: self.position.y -= self.SPEED
        elif self.current_orientation == 2: self.position.y += self.SPEED
        elif self.current_orientation == 3: self.position.x -= self.SPEED
        elif self.current_orientation == 4: self.position.x += self.SPEED

    def _handle_moviment(self, pacman, all_ghosts):
        if self._ENVIRONMENT.game_state == GameState.GAME_OVER: return

        if self._is_on_grid():
            if not self._can_move(self.current_orientation) or self._is_intersection():
                self.current_orientation = self._choose_direction(pacman, all_ghosts)

        self._move()

    def _release_ghost(self):
        cw = self._ENVIRONMENT.cell_width
        ch = self._ENVIRONMENT.cell_height
        hr, hc = self.house_exit_pos
        self.position = pygame.Vector2(x = hc * cw + cw // 2, y = hr * ch + ch // 2)
        self.mode = self._ENVIRONMENT.get_global_ghost_mode()
        self.current_orientation = 1 
        self._exit_timer = 0

    def _enter_house(self):
        self.mode = GhostState.IN_HOUSE
        self.SPEED = self.NORMAL_SPEED

        cw = self._ENVIRONMENT.cell_width
        ch = self._ENVIRONMENT.cell_height
        hr, hc = self.house_wait_pos

        self.position = pygame.Vector2(x = hc * cw + cw / 2, y = hr * ch + ch // 2)
        self._exit_timer = pygame.time.get_ticks() + self.house_respawn_time

    def set_eaten(self):
        self.mode = GhostState.EATEN
        self.immune = True 

    def get_rect(self) -> pygame.Rect:
        collision_rect = pygame.Rect(0, 0, 32, 32)
        collision_rect.center = (int(self.position.x), int(self.position.y))
        return collision_rect

    def update(self, dt):
        if self._ENVIRONMENT.game_state == GameState.GAME_OVER: 
            return

        pacman = self._ENVIRONMENT.entities[0] 
        all_ghosts = [e for e in self._ENVIRONMENT.entities if isinstance(e, Ghost)]
        
        self._sync_global_game_state()
        self.previous_mode = self.mode
        self._determine_ghost_mode(pacman, all_ghosts)
        self._check_forced_reversal()
        self._update_animations(dt)

        if self.mode != GhostState.IN_HOUSE:
            self._handle_moviment(pacman, all_ghosts)

    def _sync_global_game_state(self):
        """Gerencia transições baseadas no estado global do jogo."""
        current_game_state = self._ENVIRONMENT.game_state
        
        if (current_game_state == GameState.VULNERABLE and 
            self.last_game_state != GameState.VULNERABLE):
            self.immune = False
            
        self.last_game_state = current_game_state

    def _determine_ghost_mode(self, pacman, all_ghosts):
        """ A máquina de estados principal do Fantasma. """
        game_mode = self._ENVIRONMENT.game_state

        if self.mode == GhostState.IN_HOUSE:
            if self._should_exit_house(pacman, all_ghosts):
                self._release_ghost()
            return 

        if self.mode == GhostState.EATEN:
            row, col = self._get_coordinates()
            hr, hc = self.house_door_pos
            if abs(row - hr) < 1 and abs(col - hc) < 1:
                self._enter_house()
            return

        if self.mode not in [GhostState.IN_HOUSE, GhostState.EXITING]:
            if game_mode == GameState.VULNERABLE:
                if self.mode != GhostState.EATEN and not self.immune:
                    self.mode = GhostState.VULNERABLE
                elif self.immune:
                     self.mode = self._ENVIRONMENT.get_global_ghost_mode()
            
            elif self.previous_mode == GhostState.VULNERABLE and game_mode != GameState.VULNERABLE:
                 self.mode = self._ENVIRONMENT.get_global_ghost_mode()
            
            elif game_mode == GameState.CHASE:
                 self.mode = self._ENVIRONMENT.get_global_ghost_mode()

    def _check_forced_reversal(self):
        """ Força o fantasma a virar 180 graus quando entra/sai do modo vulnerável. """
        if self.mode != self.previous_mode:
            is_becoming_vulnerable = self.mode == GhostState.VULNERABLE
            was_vulnerable = self.previous_mode == GhostState.VULNERABLE
            
            valid_state = self.previous_mode not in [GhostState.IN_HOUSE, GhostState.EATEN, GhostState.EXITING]

            if (is_becoming_vulnerable or was_vulnerable) and valid_state:
                self.current_orientation = self.opposite_orientation[self.current_orientation]

    def _update_animations(self, dt):
        """ Gerencia a troca de sprites. """
        if self.mode == GhostState.VULNERABLE:
            self._vulnerable_animation_timer += dt
            if self._vulnerable_animation_timer >= self._vulnerable_animation_speed:
                self._vulnerable_animation_timer -= self._vulnerable_animation_speed
                self._vulnerable_animation_frame = (self._vulnerable_animation_frame + 1) % len(self._vulnerable_sprites)
        
        elif self.mode in [GhostState.CHASE, GhostState.SCATTER]:
            pass 

    def draw(self, screen):
        """ Desenha o fantasma na tela. """
        x, y = int(self.position.x), int(self.position.y)
        current_sprite = None

        if self.mode == GhostState.VULNERABLE:
            current_sprite = self._vulnerable_sprites[self._vulnerable_animation_frame]
        elif self.mode == GhostState.EATEN:
            current_sprite = self._eaten_sprites.get(self.current_orientation)
        else:
            current_sprite = self._sprites.get(self.current_orientation)

        if current_sprite: 
            rectangle = current_sprite.get_rect(center=(x, y))
            screen.blit(current_sprite, rectangle)

    def get_ghost(self, all_ghosts, cls):
        """ Retorna um fantasma. """
        return next((g for g in all_ghosts if isinstance(g, cls)), None)
    
    def reset(self):
        self.position = self.start_pos.copy()
        self.current_orientation = 4
        self.mode = self.start_mode
        self.SPEED = self.NORMAL_SPEED
        self._exit_timer = 0
        self.immune = False

        if self.mode == GhostState.SCATTER:
            self._release_ghost()