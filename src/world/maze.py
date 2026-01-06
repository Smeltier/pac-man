import math

import pygame

class Maze: 

    _wall_color: str
    _door_color: str
    _small_pellet_color: str
    _power_pellet_color: str
    _small_pellet_radius: int
    _power_pellet_radius: int
    _wall_codes: dict 
    _cell_width: int
    _cell_height: int
    _maze_rows: int
    _maze_cols: int
    _maze_layout: list[list[int]]
    _matrix: list[list[int]]
    _total_tablets: int
    _wall_surface: pygame.Surface

    def __init__(self, maze_file: str, cell_width: int, cell_height: int, config: dict):
        colors = config.get("colors", {})
        self._wall_color = colors.get("wall", "blue")
        self._door_color = colors.get("door", "white")
        self._small_pellet_color = colors.get("small_pellet", "white")
        self._power_pellet_color = colors.get("power_pellet", "blue")

        radius = config.get("radius", {})
        self._small_pellet_radius = radius.get("small_pellet", 2)
        self._power_pellet_radius = radius.get("power_pellet", 6)

        codes = config.get("codes", {})
        self._wall_codes = {
            "vertical": codes.get("vertical", 3),
            "horizontal": codes.get("horizontal", 4),
            "arc_tl": codes.get("arc_tl", 5),
            "arc_tr": codes.get("arc_tr", 6),
            "arc_br": codes.get("arc_br", 7),
            "arc_bl": codes.get("arc_bl", 8),
            "door": codes.get("door", 9)
        }
        
        self._cell_width = cell_width
        self._cell_height = cell_height

        self._maze_layout = self._load_maze_layout(maze_file)
        self._maze_rows = len(self._maze_layout)
        self._maze_cols = len(self._maze_layout[0])

        self._matrix = self._load_wall_matrix()
        self._total_tablets = self._count_tablets()

        self._wall_surface = self._create_wall_surface()

    def eat_tablet(self) -> None:
        """ Decrementa o contador de pastilhas de forma segura. """
        if self._total_tablets > 0:
            self._total_tablets -= 1
            
    def is_level_cleared(self) -> bool:
        """ Verifica se todas as pastilhas foram comidas. """
        return self._total_tablets <= 0

    def _load_maze_layout(self, maze_file: str) -> list[list[int]]:
        maze = []

        try:
            with open(maze_file, 'r') as f:
                for line in f:
                    maze.append([int(x) for x in line.split()])
        except FileNotFoundError:
            return [[0]] 

        return maze
    
    def _load_wall_matrix(self) -> list[list[int]]:
        matrix = []
        for row in self._maze_layout:
            new_row = [-1 if x > 2 else x for x in row]
            matrix.append(new_row)
        return matrix
    
    def _count_tablets(self) -> int:
        count = 0
        for row in self._matrix:
            for cell in row:
                if cell == 1 or cell == 2:
                    count += 1
        return count
    
    def _create_wall_surface(self) -> pygame.Surface:
        """ Gera uma imagem estática das paredes para não recalcular todo frame. """
        surface = pygame.Surface((self._maze_cols * self._cell_width, self._maze_rows * self._cell_height))
        surface.set_colorkey('black')
        
        wc = self._wall_codes
        wall_color = self._wall_color
        door_color = self._door_color
        cw, ch = self._cell_width, self._cell_height

        for row in range(self._maze_rows):
            for col in range(self._maze_cols):

                x, y = col * cw, row * ch
                cell_code = self._maze_layout[row][col]
                
                if cell_code == wc["vertical"]:
                    pygame.draw.line(surface, wall_color, (x + cw // 2, y), (x + cw // 2, y + ch))

                elif cell_code == wc["horizontal"]:
                    pygame.draw.line(surface, wall_color, (x, y + ch // 2), (x + cw, y + ch // 2))

                elif cell_code == wc["door"]:
                    pygame.draw.line(surface, door_color, (x, y + ch // 2), (x + cw, y + ch // 2))
                
                elif cell_code == wc["arc_tl"]:
                    pygame.draw.arc(surface, wall_color, (x - cw // 2, y + ch // 2, cw, ch), 0, math.pi/2)

                elif cell_code == wc["arc_tr"]:
                    pygame.draw.arc(surface, wall_color, (x + cw // 2, y + ch // 2, cw, ch), math.pi/2, math.pi)

                elif cell_code == wc["arc_br"]:
                    pygame.draw.arc(surface, wall_color, (x + cw // 2, y - ch // 2, cw, ch), math.pi, 3*math.pi/2)

                elif cell_code == wc["arc_bl"]:
                    pygame.draw.arc(surface, wall_color, (x - cw // 2, y - ch // 2, cw, ch), 3*math.pi/2, 2*math.pi)

        return surface

    @property
    def matrix(self) -> list[list[int]]:
        return self._matrix

    @property
    def maze_layout(self) -> list[list[int]]:
        return self._maze_layout

    @property
    def wall_surface(self) -> pygame.Surface:
        return self._wall_surface

    @property
    def total_tablets(self) -> int:
        return self._total_tablets

    @property
    def rows(self) -> int:
        return self._maze_rows

    @property
    def cols(self) -> int:
        return self._maze_cols

    @property
    def cell_width(self) -> int:
        return self._cell_width

    @property
    def cell_height(self) -> int:
        return self._cell_height

    @property
    def wall_color(self) -> str:
        return self._wall_color

    @property
    def door_color(self) -> str:
        return self._door_color

    @property
    def small_pellet_color(self) -> str:
        return self._small_pellet_color

    @property
    def power_pellet_color(self) -> str:
        return self._power_pellet_color
    
    @property
    def small_pellet_radius(self) -> int:
        return self._small_pellet_radius
    
    @property
    def power_pellet_radius(self) -> int:
        return self._power_pellet_radius