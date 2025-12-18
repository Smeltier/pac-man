import pygame

from abc import ABC as AbstractClass, abstractmethod

class Entity (AbstractClass):
    
    def __init__(self, x, y, environment):
        self._position = pygame.Vector2((x, y))
        self._environment = environment

    @abstractmethod
    def update(self, delta_time) -> None:
        raise NotImplementedError("A subclasse deve implementar update")
    
    @abstractmethod
    def draw(self, screen) -> None:
        raise NotImplementedError("A subclasse deve implementar draw")
    
    @abstractmethod
    def reset(self) -> None:
        raise NotImplementedError("A subclasse deve implementar reset")

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, new_position):
        self._position = new_position