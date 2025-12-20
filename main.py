import pygame
import json
import os

from src.core.environment import Environment
from src.core.settings import Settings
from src.entities.pacman import PacMan
from src.entities.blinky import Blinky
from src.entities.clyde import Clyde
from src.entities.pinky import Pinky
from src.entities.inky import Inky

def load_image(path: str, scale: tuple = None) -> pygame.Surface:
    try:
        full_path = os.path.join("src", "data", "images", path)
        image = pygame.image.load(full_path).convert_alpha()
        if scale:
            image = pygame.transform.scale(image, scale)

        return image
    except FileNotFoundError:
        print(f"[ERRO] Imagem não encontrada: {path}")
        return pygame.Surface((32, 32))

def get_pacman_assets(cw: int, ch: int) -> dict:
    scale = (cw, ch)
    
    sprites_list = [
        load_image("pacman_eat_0.png", scale),
        load_image("pacman_eat_1.png", scale),
        load_image("pacman_eat_2.png", scale)
    ]

    return { "move": sprites_list }

def get_ghost_assets(ghost_name: str, cw: int, ch: int) -> dict:
    scale = (cw, ch)
    
    return {
        "directional": {
            1: load_image(f"{ghost_name}_up.png", scale),
            2: load_image(f"{ghost_name}_down.png", scale),
            3: load_image(f"{ghost_name}_left.png", scale),
            4: load_image(f"{ghost_name}_right.png", scale)
        },
        "vulnerable": [
            load_image("vulnerable_sprite.png", scale),
            load_image("vulnerable_sprite_white.png", scale)
        ],
        "eaten": {
            1: load_image("eyes_up.png", scale),
            2: load_image("eyes_down.png", scale),
            3: load_image("eyes_left.png", scale),
            4: load_image("eyes_right.png", scale)
        }
    }

def main():
    pygame.init()
    pygame.mixer.init()

    pygame.display.set_caption("Pac-Man")

    FPS = 60
    WIDTH, HEIGHT = 900, 950
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()

    settings = Settings('src/data/settings/config.json')
    
    teleport_config: dict = settings.get("teleport", {})
    ghost_config: dict = settings.get("ghost", {})
    audio_manager_config: dict = settings.get("audio_manager", {})
    environment_config: dict = settings.get("environment", {})
    maze_config: dict = settings.get("maze", {})
    hud_config: dict = settings.get("hud", {})
    pacman_config: dict = settings.get("pacman", {})
    blinky_config: dict = settings.get("blinky", {})
    inky_config: dict = settings.get("inky", {})
    clyde_config: dict = settings.get("clyde", {})
    pinky_config: dict = settings.get("pinky", {})

    environment = Environment(
        screen=SCREEN, 
        maze_file='src/data/settings/default_maze.txt', 
        config=environment_config | maze_config | audio_manager_config | hud_config
    )

    cw, ch = environment.cell_width, environment.cell_height
    pacman_start_pos = pacman_config.get("start_grid_pos", [18, 15])
    start_row, start_col = pacman_start_pos[0], pacman_start_pos[1]

    pacman = PacMan(
        x = start_col * cw + cw // 2, 
        y = start_row * ch + ch // 2, 
        environment = environment,
        config = teleport_config | pacman_config,
        assets = get_pacman_assets(cw, ch)
    )
    environment.add_entity(pacman)

    blinky = Blinky(
        x = 15 * cw + cw // 2,
        y = 12 * ch + ch // 2,
        environment = environment,
        config = teleport_config | ghost_config | blinky_config,
        assets = get_ghost_assets("blinky", cw, ch)
    )
    environment.add_entity(blinky)

    pinky = Pinky(
        x = 15 * cw + cw // 2,
        y = 15 * ch + ch // 2,
        environment = environment,
        config = teleport_config | ghost_config | pinky_config,
        assets = get_ghost_assets("pinky", cw, ch)
    )
    environment.add_entity(pinky)

    inky = Inky(
        x = 13 * cw + cw // 2,
        y = 15 * ch + ch // 2,
        environment = environment,
        config = teleport_config | ghost_config | inky_config,
        assets = get_ghost_assets("inky", cw, ch)
    )
    environment.add_entity(inky)

    clyde = Clyde(
        x = 17 * cw + cw // 2,
        y = 15 * ch + ch // 2,
        environment = environment,
        config = teleport_config | ghost_config | clyde_config,
        assets = get_ghost_assets("clyde", cw, ch)
    )
    environment.add_entity(clyde)

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

if __name__ == "__main__":
    main()