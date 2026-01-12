import pygame
from src.core.states import GhostState

class GhostDirector:

    _chase_duration_ms: int
    _scatter_duration_ms: int
    _current_mode: GhostState
    _last_switch_time: int
    _paused: bool

    def __init__(self, config: dict):
        env_config = config.get("environment", {})
        durations = env_config.get("durations_ms", {})
        
        self._chase_duration_ms = durations.get("chase", 20000)
        self._scatter_duration_ms = durations.get("scatter", 7000)
        
        self._current_mode = GhostState.SCATTER
        self._last_switch_time = 0
        self._paused = False

    def update(self, current_time_ms: int) -> None:
        """ Verifica se é hora de trocar de modo. """
        if self._paused:
            self._last_switch_time = current_time_ms
            return

        time_since_switch = current_time_ms - self._last_switch_time

        if self._current_mode == GhostState.SCATTER:
            if time_since_switch > self._scatter_duration_ms:
                self._switch_mode(GhostState.CHASE, current_time_ms)
                
        elif self._current_mode == GhostState.CHASE:
            if time_since_switch > self._chase_duration_ms:
                self._switch_mode(GhostState.SCATTER, current_time_ms)

    def reset(self):
        """ Reinicia o ciclo para o início do nível. """
        self._current_mode = GhostState.SCATTER
        self._last_switch_time = pygame.time.get_ticks()
        self._paused = False

    def set_paused(self, is_paused: bool):
        """ Pausa o ciclo. """
        self._paused = is_paused

    def _switch_mode(self, new_mode: GhostState, time_ms: int):
        self._current_mode = new_mode
        self._last_switch_time = time_ms

    @property
    def current_mode(self) -> GhostState:
        return self._current_mode

    @property
    def is_paused(self) -> bool:
        return self._paused