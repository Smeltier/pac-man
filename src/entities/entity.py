from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from src.core.game_manager import GameManager

class Entity(ABC):
    """ Classe abstrata base para as entidades do jogo. """

    _start_position: pygame.Vector2
    _position: pygame.Vector2
    _manager: "GameManager"
    
    _teleport_x_limits: tuple[int, int] 
    _teleport_x_wrap: tuple[int, int]
    _collision_rect_size: int
    
    def __init__(self, x: float, y: float, manager: "GameManager", config: dict) -> None:
        self._start_position = pygame.Vector2(x, y)
        self._position = pygame.Vector2(x, y)
        self._manager = manager

        self._teleport_x_limits = (config.get("min_x", 0), config.get("max_x", 0))
        self._teleport_x_wrap = (config.get("wrap_x_min", 0), config.get("wrap_x_max", 0))
        
        self._collision_rect_size = config.get("collision_rect_size", 32)

    @abstractmethod
    def update(self, delta_time: float) -> None:
        """ Atualiza o estado da entidade. """
        pass
    
    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """ 
        A Entidade desenha a si mesma na superfície fornecida.
        """
        pass
    
    def reset(self) -> None:
        """ Reseta a entidade. """
        self._position = self._start_position.copy() 

    @property
    def rect(self) -> pygame.Rect:
        """ 
        Retorna o retângulo de colisão baseado na posição atual. 
        Centraliza o rect na posição (x, y).
        """
        rect = pygame.Rect(0, 0, self._collision_rect_size, self._collision_rect_size)
        rect.center = (int(self._position.x), int(self._position.y))
        return rect

    def _handle_teleport(self) -> None:
        """ Lida com o teleporte da entidade (túnel). """
        min_x, max_x = self._teleport_x_limits
        wrap_min, wrap_max = self._teleport_x_wrap

        if self._position.x <= min_x: 
            self._position.x = wrap_min
        elif self._position.x >= max_x: 
            self._position.x = wrap_max

    @property
    def position(self) -> pygame.Vector2:
        return self._position
    
    @position.setter
    def position(self, new_position: pygame.Vector2) -> None:
        self._position = new_position

    @property
    def rect(self) -> pygame.Rect:
        """ Retorna o retângulo de colisão. """
        rect = pygame.Rect(0, 0, self._collision_rect_size, self._collision_rect_size)
        rect.center = (int(self._position.x), int(self._position.y))
        return rect
        
    @property
    def start_position(self) -> pygame.Vector2:
        """ Posição inicial (spawn). """
        return self._start_position