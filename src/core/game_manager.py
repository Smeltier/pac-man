import pygame

from src.core.ghost_director import GhostDirector
from src.core.audio_manager import AudioManager
from src.ui.game_renderer import GameRenderer
from src.core.states import GhostState
from src.core.states import GameState
from src.world.maze import Maze
from src.ui.hud import HUD

class GameManager: 

    _ghost_director: GhostDirector
    _renderer: GameRenderer
    _audio_manager: AudioManager
    _maze: Maze
    _hud: HUD
    _screen: pygame.Surface
    _game_state: GameState
    _entities: list
    _lives_remaining: int
    _initial_lives: int
    _vulnerable_duration_ms: int
    _game_over_screen_duration_ms: int
    _vulnerable_timer_ms: int
    _game_over_start_time_ms: int

    def __init__(self, screen: pygame.Surface, maze_file: str, config: dict):
        self._screen = screen
        
        env_config: dict = config.get("environment", {})
        durations: dict = env_config.get("durations_ms", {})
        
        self._initial_lives = env_config.get("initial_lives", 3)
        self._lives_remaining = self._initial_lives
        
        self._vulnerable_duration_ms = durations.get("vulnerable", 7000)
        self._game_over_screen_duration_ms = durations.get("game_over_screen", 4000)

        self._game_state = GameState.CHASE
        self._entities = []
        self._vulnerable_timer_ms = 0
        self._game_over_start_time_ms = 0

        cell_width  = screen.get_width() // 30
        cell_height = screen.get_height() // 32

        self._maze = Maze(maze_file, cell_width, cell_height, config)
        self._hud = HUD(screen, config)
        self._audio_manager = AudioManager(config)
        self._ghost_director = GhostDirector(config)
        self._renderer = GameRenderer(screen)

        self._audio_manager.play_chase()

    def update(self, delta_time: float) -> None:
        current_time = pygame.time.get_ticks()

        if self._game_state in [GameState.GAME_OVER, GameState.VICTORY]:
            self._handle_end_game_timer()
            return 

        if self._game_state == GameState.VULNERABLE:
            self._check_vulnerable_timeout()
            self._ghost_director.set_paused(True)
        else:
            self._ghost_director.set_paused(False)
            self._ghost_director.update(current_time)
        
        for entity in self._entities[:]:
            entity.update(delta_time)

    def draw(self) -> None:
        current_score = 0

        if self._entities:
             current_score = self._entities[0].total_points

        self._renderer.render(
            maze=self._maze,
            entities=self._entities,
            hud=self._hud,
            game_state=self._game_state,
            score=current_score,
            lives=self._lives_remaining
        )

    def add_entity(self, entity) -> None:
        if entity is None: raise ValueError('Entidade inválida.')
        if entity not in self._entities: self._entities.append(entity)
    
    def remove_entity(self, entity) -> None:
        self._entities = [e for e in self._entities if e is not entity]

    def set_vulnerable(self) -> None:
        if self._game_state in (GameState.GAME_OVER, GameState.VICTORY): return

        if self._game_state != GameState.VULNERABLE:
            self._game_state = GameState.VULNERABLE
            self._audio_manager.play_vulnerable()

        self._vulnerable_timer_ms = pygame.time.get_ticks()
    
    def set_chase(self) -> None:
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

    def get_global_ghost_mode(self) -> GhostState:
        return self._ghost_director.current_mode

    def _reset_level(self):
        pygame.time.delay(1000) 
        self.set_chase()
        
        self._ghost_director.reset()

        for entity in self._entities:
            if hasattr(entity, 'reset'):
                entity.reset()

    def _handle_end_game_timer(self):
        now = pygame.time.get_ticks()

        if now - self._game_over_start_time_ms > self._game_over_screen_duration_ms:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def _check_vulnerable_timeout(self):
        now = pygame.time.get_ticks()

        if now - self._vulnerable_timer_ms > self._vulnerable_duration_ms:
            self.set_chase()

    @property
    def game_state(self) -> GameState:
        return self._game_state

    @property
    def lives(self) -> int:
        return self._lives_remaining

    @property
    def entities(self) -> list:
        return self._entities

    @property
    def maze(self) -> Maze:
        return self._maze

    @property
    def audio_manager(self) -> AudioManager:
        return self._audio_manager

    @property
    def renderer(self) -> GameRenderer:
        return self._renderer

    @property
    def ghost_director(self) -> GhostDirector:
        return self._ghost_director

    @property
    def matrix(self) -> list[list[int]]:
        return self._maze.matrix

    @property
    def cell_width(self) -> int:
        return self._maze.cell_width

    @property
    def cell_height(self) -> int:
        return self._maze.cell_height
    
    @property
    def screen_width(self) -> int:
        return self._screen.get_width()
        
    @property
    def screen_height(self) -> int:
        return self._screen.get_height()