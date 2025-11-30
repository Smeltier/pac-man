import pygame

class Game ():

    def __init__ (self, width, height, fps) -> None:
        pygame.init()
        pygame.mixer.init()

        self.width: float  = width
        self.height: float = height
        self.fps: int      = fps
        self.running: bool = True

    