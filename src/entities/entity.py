import pygame

class Entity ():

    def __init__(self, x, y, environment):
        self.position = pygame.Vector2((x, y))
        self._ENVIRONMENT = environment