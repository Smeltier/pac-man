import pygame

from environment import Environment
from pacman import PacMan

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

environment.add_entity(
    PacMan (
        x = 15 * environment.cell_width + environment.cell_width // 2, 
        y = 18 * environment.cell_height + environment.cell_height // 2, 
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