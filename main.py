import pygame

from src.core.settings import Settings
from src.core.environment import Environment
from src.entities.pacman import PacMan
from src.entities.blinky import Blinky
from src.entities.clyde import Clyde
from src.entities.pinky import Pinky
from src.entities.inky import Inky

pygame.init()
pygame.mixer.init()

game_title: str = "Pac-Man"
pygame.display.set_caption(game_title)

FPS = 60
WIDTH, HEIGHT = 900, 950
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

settings = Settings('src/data/settings/config.json')
teleport_data = settings.get("teleport")

environment = Environment(
    screen = SCREEN, 
    maze_file = 'src/data/settings/default_maze.txt',
)

cw = environment.cell_width
ch = environment.cell_height

pacman_data = settings.get("pacman")
pacman_config = pacman_data | teleport_data

environment.add_entity(
    PacMan (
        x = 15 * cw + cw // 2, 
        y = 18 * ch + ch // 2, 
        environment = environment,
        config = pacman_config
    )
)

environment.add_entity(
    Blinky (
        x = 15 * cw + cw // 2,
        y = 12 * ch + ch // 2,
        environment = environment,
        ghost_config = config_container.ghost,
        blinky_config = config_container.blinky,
        teleport_config = config_container.teleport
    )
)

environment.add_entity(
    Pinky (
        x = 15 * cw + cw // 2,
        y = 14 * ch + ch // 2,
        environment = environment,
        ghost_config = config_container.ghost,
        pinky_config = config_container.pinky,
        teleport_config = config_container.teleport
    )
)

environment.add_entity(
    Inky (
        x = 13 * cw + cw // 2,
        y = 14 * ch + ch // 2,
        environment = environment,
        ghost_config = config_container.ghost,
        inky_config = config_container.inky,
        teleport_config = config_container.teleport
    )
)

environment.add_entity(
    Clyde (
        x = 17 * cw + cw // 2,
        y = 14 * ch + ch // 2,
        environment = environment,
        ghost_config = config_container.ghost,
        clyde_config = config_container.clyde,
        teleport_config = config_container.teleport
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