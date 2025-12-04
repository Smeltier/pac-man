import math
import pygame

from src.data.class_config.maze_config import MazeConfig

class Maze (): 

    def __init__ (self, maze_file: str, cell_width: int, cell_height: int, maze_config: MazeConfig):

        self.WALL_COLOR = maze_config.WALL_COLOR
        self.DOOR_COLOR = maze_config.DOOR_COLOR
        self.SMALL_PELLET_COLOR = maze_config.SMALL_PELLET_COLOR
        self.POWER_PELLET_COLOR = maze_config.POWER_PELLET_COLOR
        self.SMALL_PELLET_RADIUS = maze_config.SMALL_PELLET_RADIUS
        self.POWER_PELLET_RADIUS = maze_config.POWER_PELLET_RADIUS
        self.WALL_CODE_VERTICAL = maze_config.WALL_CODE_VERTICAL
        self.WALL_CODE_HORIZONTAL = maze_config.WALL_CODE_HORIZONTAL
        self.WALL_CODE_ARC_TL = maze_config.WALL_CODE_ARC_TL
        self.WALL_CODE_ARC_TR = maze_config.WALL_CODE_ARC_TR
        self.WALL_CODE_ARC_BR = maze_config.WALL_CODE_ARC_BR
        self.WALL_CODE_ARC_BL = maze_config.WALL_CODE_ARC_BL
        self.WALL_CODE_DOOR = maze_config.WALL_CODE_DOOR
        
        self._cell_width  = cell_width
        self._cell_height = cell_height

        self._maze_layout = self._load_maze_layout(maze_file)
        self._maze_rows   = len(self._maze_layout)
        self._maze_cols   = len(self._maze_layout[0])

        self._matrix        = self._load_wall_matrix()
        self._total_tablets = self._count_tablets()

        self._wall_surface = self._create_wall_surface()

    # MÉTODOS PÚBLICOS

    def draw_walls (self, screen):
        screen.blit(self._wall_surface, (0, 0))

    def draw_tablets (self, screen):
        color = self.SMALL_PELLET_COLOR

        for row in range(self._maze_rows):
            for col in range(self._maze_cols):
                x, y = col * self._cell_width, row * self._cell_height

                if self._matrix[row][col] == 1:
                    x += self._cell_height // 2
                    y += self._cell_width // 2
                    pygame.draw.circle(screen, color, (x, y), self.SMALL_PELLET_RADIUS)

                if self._matrix[row][col] == 2:
                    x += self._cell_height // 2
                    y += self._cell_width // 2
                    pygame.draw.circle(screen, color, (x, y), self.POWER_PELLET_RADIUS)
    
    @property
    def matrix(self):
        return self._matrix
    
    @property
    def total_tablets(self):
        return self._total_tablets
    
    # @total_tablets.setter
    # def total_tablets(self, value):
    #     self._total_tablets = value
    
    @property
    def cell_width(self):
        return self._cell_width
    
    @property
    def cell_height(self):
        return self._cell_height

    @property
    def maze_layout(self):
        return self._maze_layout

    # MÉTODOS PRIVADOS

    def _load_maze_layout (self, maze_file: str) -> list[list[int]]:
        maze = []
        with open(maze_file, 'r') as f:
            for line in f:
                row = [int(x) for x in line.split()]
                maze.append(row)
                
        return maze
    
    def _load_wall_matrix (self) -> list[list[int]]:
        matrix = []
        for row in self._maze_layout:
            new_row = [-1 if x > 2 else x for x in row]
            matrix.append(new_row)

        return matrix
    
    def _count_tablets (self) -> int:
        count = 0
        for row in range(self._maze_rows):
            for col in range(self._maze_cols):
                if self._matrix[row][col] == 1 or self._matrix[row][col] == 2:
                    count += 1

        return count
    
    def _create_wall_surface (self) -> pygame.Surface:
        surface = pygame.Surface((self._maze_cols * self._cell_width, self._maze_rows * self._cell_height))
        surface.set_colorkey('black')

        wall_color = self.WALL_COLOR

        for row in range(self._maze_rows):
            for col in range(self._maze_cols):
                x, y = col * self._cell_width, row * self._cell_height
                cell_code = self._maze_layout[row][col]
                
                if cell_code == self.WALL_CODE_VERTICAL:
                    x += self._cell_height // 2
                    pygame.draw.line(surface, wall_color, (x, y), (x, y + self._cell_height))

                elif cell_code == self.WALL_CODE_HORIZONTAL:
                    y += self._cell_width // 2
                    pygame.draw.line(surface, wall_color, (x, y), (x + self._cell_height, y))

                elif cell_code == self.WALL_CODE_ARC_TL:
                    x -= self._cell_height // 2
                    y += self._cell_width // 2
                    pygame.draw.arc(surface, wall_color, (x, y, self._cell_height, self._cell_width), 0, math.pi / 2)

                elif cell_code == self.WALL_CODE_ARC_TR:
                    x += self._cell_height // 2
                    y += self._cell_width // 2
                    pygame.draw.arc(surface, wall_color, (x, y, self._cell_height, self._cell_width), math.pi / 2, math.pi)

                elif cell_code == self.WALL_CODE_ARC_BR:
                    x += self._cell_height // 2
                    y -= self._cell_width // 2
                    pygame.draw.arc(surface, wall_color, (x, y, self._cell_height, self._cell_width), math.pi, 3 * math.pi / 2)

                elif cell_code == self.WALL_CODE_ARC_BL:
                    x -= self._cell_height // 2
                    y -= self._cell_width // 2
                    pygame.draw.arc(surface, wall_color, (x, y, self._cell_height, self._cell_width), 3 * math.pi / 2, 2 * math.pi)

                elif cell_code == self.WALL_CODE_DOOR:
                    y += self._cell_width // 2
                    pygame.draw.line(surface, self.DOOR_COLOR, (x, y), (x + self._cell_height, y))

        return surface