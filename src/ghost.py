import pygame

from entity import Entity

class Ghost (Entity):
    
    def __init__(self, x, y, environment):
        super().__init__(x, y, environment)