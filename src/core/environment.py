import pygame

from src.data.class_config.audio_manager_config import AudioManagerConfig   
from src.data.class_config.environment_config import EnvironmentConfig
from src.data.class_config.hud_config import HUDConfig
from src.data.class_config.maze_config import MazeConfig
from src.core.states import GameState
from src.core.states import GhostState
from src.core.audio_manager import AudioManager
from src.world.maze import Maze
from src.ui.hud import HUD

class Environment ():

    def __init__ (self, screen, maze_file: str, environment_config: EnvironmentConfig, hud_config: HUDConfig, audio_manager_config: AudioManagerConfig, maze_config: MazeConfig):

        self.VULNERABLE_DURATION_MS = environment_config.VULNERABLE_DURATION_MS
        self.CHASE_DURATION_MS = environment_config.CHASE_DURATION_MS
        self.SCATTER_DURATION_MS = environment_config.SCATTER_DURATION_MS
        self.GAME_OVER_SCREEN_DURATION_MS = environment_config.GAME_OVER_SCREEN_DURATION_MS
        self.INITIAL_LIVES = environment_config.INITIAL_LIVES

        self._screen = screen
        self._game_state = GameState.CHASE
        self._entities = []
        self._lives_remaining = self.INITIAL_LIVES

        self._vulnerable_timer_ms = 0
        self._game_over_start_time_ms = 0
        self._global_mode_change_time_ms = 0
        self._current_global_ghost_mode = GhostState.SCATTER

        cell_width  = screen.get_width() // 30
        cell_height = screen.get_height() // 32

        self._maze = Maze(maze_file, cell_width, cell_height, maze_config)
        self._hud  = HUD(screen, hud_config)
        self._audio_manager = AudioManager(audio_manager_config)

        self._maze_matrix = self._maze.matrix
        self._cell_width = self._maze.cell_width
        self._cell_height = self._maze.cell_height

        self._audio_manager.play_chase()

    def update(self, delta_time: float) -> None:
        if self._game_state in [GameState.GAME_OVER, GameState.VICTORY]:
            self._handle_end_game_timer()
            return 

        if self._game_state == GameState.VULNERABLE:
            self._check_vulnerable_timeout()
        
        for entity in self._entities[:]:
            entity.update(delta_time)

    def draw (self) -> None:
        self._screen.fill('black')
        
        self._maze.draw_walls(self._screen)
        self._maze.draw_tablets(self._screen)
        
        for entity in self._entities:
            entity.draw(self._screen)
            
        if self._entities:
            player_score = self._entities[0].total_points
            self._hud.draw_score(player_score, self._lives_remaining)
        
        if self._game_state == GameState.GAME_OVER:
            self._hud.draw_game_over()
        
        if self._game_state == GameState.VICTORY:
            self._hud.draw_victory()

    def add_entity (self, entity) -> None:
        if entity is None:
            raise ValueError('Entidade inválida.')

        if entity not in self._entities:
            self._entities.append(entity)
    
    def remove_entity (self, entity) -> None:
        self._entities = [e for e in self._entities if e is not entity]

    def set_vulnerable(self) -> None:
        if self._game_state in (GameState.GAME_OVER, GameState.VICTORY):
            return

        if self._game_state != GameState.VULNERABLE:
            self._game_state = GameState.VULNERABLE
            self._audio_manager.play_vulnerable()

        self._vulnerable_timer_ms = pygame.time.get_ticks()
    
    def set_chase (self) -> None:
        self._game_state = GameState.CHASE
        self._audio_manager.play_chase()

    def handle_player_death(self):
        self._lives_remaining -= 1

        if self._lives_remaining > 0:
            self._reset_level()
        else:
            self._game_state = GameState.GAME_OVER
            self._game_over_start_time_ms = pygame.time.get_ticks()

    def handle_victory(self):
        self._game_state = GameState.VICTORY
        
        self._audio_manager.stop_waka() 
        pygame.mixer.music.stop() 
        
        self._game_over_start_time_ms = pygame.time.get_ticks()

    def get_global_ghost_mode (self) -> GhostState:
        now = pygame.time.get_ticks()

        if self._current_global_ghost_mode == GhostState.SCATTER:
            if now - self._global_mode_change_time_ms > self.SCATTER_DURATION_MS:
                self._current_global_ghost_mode = GhostState.CHASE
                self._global_mode_change_time_ms = now
        else:
            if now - self._global_mode_change_time_ms > self.CHASE_DURATION_MS:
                self._current_global_ghost_mode = GhostState.SCATTER
                self._global_mode_change_time_ms = now

        return self._current_global_ghost_mode
    
    @property
    def game_state(self):
        return self._game_state
    
    @property
    def matrix(self):
        return self._maze_matrix
    
    @property
    def cell_width(self):
        return self._cell_width
    
    @property
    def cell_height(self):
        return self._cell_height
    
    @property
    def entities(self):
        return self._entities
    
    @property
    def audio_manager(self):
        return self._audio_manager
    
    @property
    def maze(self):
        return self._maze

    def _reset_level(self):
        pygame.time.delay(1000) 
        self.set_chase()
        self._global_mode_change_time_ms = pygame.time.get_ticks()
        self._current_global_ghost_mode = GhostState.SCATTER

        for entity in self._entities:
            if hasattr(entity, 'reset'):
                entity.reset()

    def _handle_end_game_timer(self):
        now = pygame.time.get_ticks()
        if now - self._game_over_start_time_ms > self.GAME_OVER_SCREEN_DURATION_MS:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def _check_vulnerable_timeout(self):
        now = pygame.time.get_ticks()
        if now - self._vulnerable_timer_ms > self.VULNERABLE_DURATION_MS:
            self.set_chase()