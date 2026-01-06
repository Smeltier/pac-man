import sys
import os

import pygame

from src.core.game_manager import GameManager
from src.entities.pacman import PacMan
from src.core.settings import Settings
from src.entities.blinky import Blinky
from src.entities.clyde import Clyde
from src.entities.pinky import Pinky
from src.entities.inky import Inky

class Game:

    _width: float
    _height: float
    _fps: int
    _running: bool

    def __init__(self, width: float, height: float, fps: int) -> None:
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Pac-Man")

        self._width: float = width
        self._height: float = height
        self._fps: int = fps

        self._running: bool = True
        self._screen = pygame.display.set_mode((width, height))
        self._clock = pygame.time.Clock()

    def run(self, config_path: str) -> None:

        game_manager = self._initial_config(config_path)

        while self._running:
            delta_time: float = self._clock.tick(self._fps) / 1000.0

            self._handle_event()

            game_manager.update(delta_time)
            game_manager.draw()

            pygame.display.flip()

        pygame.quit()

    def _handle_event(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False

    def _initial_config(self, config_path: str) -> GameManager:

        if getattr(sys, 'frozen', False):
            BASE_DIR = os.path.dirname(sys.executable)
        else:
            BASE_DIR = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..")
            )

        def load_image(path: str, scale: tuple = None) -> pygame.Surface:
            try:
                full_path = os.path.join(BASE_DIR, "data", "images", path)
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

        settings = Settings(config_path)

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

        maze_file_path = os.path.join(BASE_DIR, 'data', 'settings', 'default_maze.txt')

        game_manager = GameManager(
            screen = self._screen, 
            maze_file = maze_file_path, 
            config = environment_config | maze_config | audio_manager_config | hud_config
        )

        cw, ch = game_manager.cell_width, game_manager.cell_height
        pacman_start_pos = pacman_config.get("start_grid_pos", [18, 15])
        start_row, start_col = pacman_start_pos[0], pacman_start_pos[1]

        game_manager.add_entity(
            PacMan(
                x = start_col * cw + cw // 2, 
                y = start_row * ch + ch // 2, 
                manager = game_manager,
                config = teleport_config | pacman_config,
                assets = get_pacman_assets(cw, ch)
            )
        )

        game_manager.add_entity(
            Blinky(
                x = 15 * cw + cw // 2,
                y = 12 * ch + ch // 2,
                manager = game_manager,
                config = teleport_config | ghost_config | blinky_config,
                assets = get_ghost_assets("blinky", cw, ch)
            )
        )

        game_manager.add_entity(
            Pinky(
                x = 15 * cw + cw // 2,
                y = 15 * ch + ch // 2,
                manager = game_manager,
                config = teleport_config | ghost_config | pinky_config,
                assets = get_ghost_assets("pinky", cw, ch)
            )
        )

        game_manager.add_entity(
            Inky(
                x = 13 * cw + cw // 2,
                y = 15 * ch + ch // 2,
                manager = game_manager,
                config = teleport_config | ghost_config | inky_config,
                assets = get_ghost_assets("inky", cw, ch)
            )
        )

        game_manager.add_entity(
            Clyde(
                x = 17 * cw + cw // 2,
                y = 15 * ch + ch // 2,
                manager = game_manager,
                config = teleport_config | ghost_config | clyde_config,
                assets = get_ghost_assets("clyde", cw, ch)
            )
        )

        return game_manager