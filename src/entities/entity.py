import pygame

class Entity ():

    def __init__(self, x, y, environment):
        
        self._position = pygame.Vector2((x, y))
        self._ENVIRONMENT = environment

    # MÉTODOS PÚBLICOS

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, new_position):
        self._position = new_position