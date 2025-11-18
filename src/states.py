from enum import Enum, auto

class GameState(Enum):
    """ Define os estados globais do jogo. """
    CHASE = auto()
    VULNERABLE = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    VICTORY = auto()

class GhostState(Enum):
    """ Define os estados dos fantasmas. """
    IN_HOUSE = auto()    
    EXITING = auto()     
    CHASE = auto()       
    SCATTER = auto()     
    VULNERABLE = auto()  
    EATEN = auto()