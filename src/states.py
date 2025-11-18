import pygame

from enum import Enum, auto

class GhostState (Enum):
    IN_HOUSE = auto()
    EXITING = auto()
    SCATTER = auto()
    CHASE = auto()
    VULNERABLE = auto()
    EATEN = auto()

class GameState (Enum):
    CHASE = auto()
    VULNERABLE = auto()
    PAUSED = auto()
    GAME_OVER = auto()