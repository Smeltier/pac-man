import pygame

from src.core.environment import Environment
from src.entities.pacman import PacMan
from src.entities.ghosts import Blinky, Pinky, Inky, Clyde
from src.entities.entity import Entity

pygame.init()
pygame.mixer.init()

game_title: str = "Pac-Man"
pygame.display.set_caption(game_title)

FPS = 60
WIDTH, HEIGHT = 900, 950
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

environment = Environment(
    screen = SCREEN, 
    maze_file = 'src/configs/maze.txt'
)

cw = environment.cell_width
ch = environment.cell_height

environment.add_entity(
    PacMan (
        x = 15 * cw + cw // 2, 
        y = 18 * ch + ch // 2, 
        environment = environment
    )
)

environment.add_entity(
    Blinky (
        x = 15 * cw + cw // 2,
        y = 12 * ch + ch // 2,
        environment = environment
    )
)

environment.add_entity(
    Pinky (
        x = 15 * cw + cw // 2,
        y = 14 * ch + ch // 2,
        environment = environment
    )
)

environment.add_entity(
    Inky (
        x = 13 * cw + cw // 2,
        y = 14 * ch + ch // 2,
        environment = environment
    )
)

environment.add_entity(
    Clyde (
        x = 17 * cw + cw // 2,
        y = 14 * ch + ch // 2,
        environment = environment
    )
)

running = True

while running:
    delta_time = CLOCK.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    environment.update(delta_time)
    environment.draw()

    pygame.display.flip()

pygame.quit()