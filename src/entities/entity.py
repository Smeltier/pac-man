from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from src.core.environment import Environment

class Entity(ABC):
    """ Classe abstrata que define uma entidade no jogo. """

    _position: pygame.Vector2
    _environment: "Environment"
    _teleport_min_x: int
    _teleport_max_x: int
    _teleport_wrap_x_min: int
    _teleport_wrap_x_max: int
    
    def __init__(self, x: float, y: float, environment: "Environment", config: dict) -> None:
        self._start_position = pygame.Vector2(x, y)
        self._position = pygame.Vector2((x, y))
        self._environment = environment

        self._teleport_min_x = config.get("min_x", 0)
        self._teleport_max_x = config.get("max_x", 0)
        self._teleport_wrap_x_min = config.get("wrap_x_min", 0)
        self._teleport_wrap_x_max = config.get("wrap_x_max", 0)

    @abstractmethod
    def update(self, delta_time: float) -> None:
        """ Atualiza a entidade com o passar de uma variação do tempo. """
        pass
    
    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """ Desenha a entidade na tela. """
        pass
    
    @abstractmethod
    def reset(self) -> None:
        """ Reseta a entidade ao final de cada rodada. """
        pass

    @property
    def position(self) -> pygame.Vector2:
        """ Retorna um Vector2 que representa a posição da Entidade. """
        return self._position
    
    @position.setter
    def position(self, new_position: pygame.Vector2) -> None:
        """ Atualiza a posição da entidade dado um novo Vector2. """
        self._position = new_position

    def _handle_teleport(self) -> None:
        """ Lida com o teleporte da entidade quando entra no portal. """
        if self.position.x <= self._teleport_min_x: 
            self.position.x = self._teleport_wrap_x_min
        if self.position.x >= self._teleport_max_x: 
            self.position.x = self._teleport_wrap_x_max