import math

import pygame

class Maze: 

    _wall_color: str
    _door_color: str
    _small_pellet_color: str
    _power_pellet_color: str
    _small_pellet_radius: int
    _power_pellet_radius: int
    _wall_code_vertical: int
    _wall_code_horizontal: int
    _wall_code_arc_tl: int
    _wall_code_arc_tr: int
    _wall_code_arc_br: int
    _wall_code_arc_bl: int
    _wall_code_door: int
    _cell_width: int
    _cell_height: int
    _maze_rows: int
    _maze_cols: int
    _maze_layout: list[list[int]]
    _matrix: list[list[int]]
    _total_tablets: int
    _wall_surface: pygame.Surface

    def __init__(self, maze_file: str, cell_width: int, cell_height: int, config: dict):
        colors_config: dict = config.get("colors", {})
        self._wall_color = colors_config.get("wall", "blue")
        self._door_color = colors_config.get("door", "white")
        self._small_pellet_color = colors_config.get("small_pellet", "white")
        self._power_pellet_color = colors_config.get("power_pellet", "blue")

        radius_config: dict = config.get("radius", {})
        self._small_pellet_radius = radius_config.get("small_pellet", 2)
        self._power_pellet_radius = radius_config.get("power_pellet", 6)

        codes_config: dict = config.get("codes", {})
        self._wall_code_vertical = codes_config.get("vertical", 3)
        self._wall_code_horizontal = codes_config.get("horizontal", 4)
        self._wall_code_arc_tl = codes_config.get("arc_tl", 5)
        self._wall_code_arc_tr = codes_config.get("arc_tr", 6)
        self._wall_code_arc_br = codes_config.get("arc_br", 7)
        self._wall_code_arc_bl = codes_config.get("arc_bl", 8)
        self._wall_code_door = codes_config.get("door", 9)
        
        self._cell_width = cell_width
        self._cell_height = cell_height

        self._maze_layout = self._load_maze_layout(maze_file)
        self._maze_rows = len(self._maze_layout)
        self._maze_cols = len(self._maze_layout[0])

        self._matrix = self._load_wall_matrix()
        self._total_tablets = self._count_tablets()

        self._wall_surface = self._create_wall_surface()

    def draw_walls(self, screen):
        screen.blit(self._wall_surface, (0, 0))

    def draw_tablets(self, screen):
        small_color = self._small_pellet_color
        power_color = self._power_pellet_color
        small_radius = self._small_pellet_radius
        power_radius = self._power_pellet_radius
        
        for row in range(self._maze_rows):
            for col in range(self._maze_cols):
                tile_value = self._matrix[row][col]

                if tile_value == 1 or tile_value == 2:
                    x = col * self._cell_width + self._cell_width // 2
                    y = row * self._cell_height + self._cell_height // 2

                    if tile_value == 1:
                        pygame.draw.circle(screen, small_color, (x, y), small_radius)
                    elif tile_value == 2:
                        pygame.draw.circle(screen, power_color, (x, y), power_radius)
    
    @property
    def matrix(self):
        return self._matrix
    
    @property
    def total_tablets(self):
        return self._total_tablets
    
    @property
    def cell_width(self):
        return self._cell_width
    
    @property
    def cell_height(self):
        return self._cell_height

    @property
    def maze_layout(self):
        return self._maze_layout

    def _load_maze_layout(self, maze_file: str) -> list[list[int]]:
        maze = []
        try:
            with open(maze_file, 'r') as f:
                for line in f:
                    row = [int(x) for x in line.split()]
                    maze.append(row)
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
        for row in range(self._maze_rows):
            for col in range(self._maze_cols):
                if self._matrix[row][col] == 1 or self._matrix[row][col] == 2:
                    count += 1
        return count
    
    def _create_wall_surface(self) -> pygame.Surface:
        surface = pygame.Surface((self._maze_cols * self._cell_width, self._maze_rows * self._cell_height))
        surface.set_colorkey('black')

        wall_color = self._wall_color
        door_color = self._door_color

        for row in range(self._maze_rows):
            for col in range(self._maze_cols):
                x, y = col * self._cell_width, row * self._cell_height
                cell_code = self._maze_layout[row][col]
                
                if cell_code == self._wall_code_vertical:
                    x += self._cell_height // 2
                    pygame.draw.line(surface, wall_color, (x, y), (x, y + self._cell_height))

                elif cell_code == self._wall_code_horizontal:
                    y += self._cell_width // 2
                    pygame.draw.line(surface, wall_color, (x, y), (x + self._cell_height, y))

                elif cell_code == self._wall_code_arc_tl:
                    x -= self._cell_height // 2
                    y += self._cell_width // 2
                    pygame.draw.arc(surface, wall_color, (x, y, self._cell_height, self._cell_width), 0, math.pi / 2)

                elif cell_code == self._wall_code_arc_tr:
                    x += self._cell_height // 2
                    y += self._cell_width // 2
                    pygame.draw.arc(surface, wall_color, (x, y, self._cell_height, self._cell_width), math.pi / 2, math.pi)

                elif cell_code == self._wall_code_arc_br:
                    x += self._cell_height // 2
                    y -= self._cell_width // 2
                    pygame.draw.arc(surface, wall_color, (x, y, self._cell_height, self._cell_width), math.pi, 3 * math.pi / 2)

                elif cell_code == self._wall_code_arc_bl:
                    x -= self._cell_height // 2
                    y -= self._cell_width // 2
                    pygame.draw.arc(surface, wall_color, (x, y, self._cell_height, self._cell_width), 3 * math.pi / 2, 2 * math.pi)

                elif cell_code == self._wall_code_door:
                    y += self._cell_width // 2
                    pygame.draw.line(surface, door_color, (x, y), (x + self._cell_height, y))

        return surface