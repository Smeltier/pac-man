import math
import pygame

class Maze ():

    def __init__ (self, maze_file: str, cell_width: int, cell_height: int):
        self.cell_width  = cell_width
        self.cell_height = cell_height
        self.wall_color  = 'blue' 

        self.maze_layout = self._load_maze_layout(maze_file)
        self.maze_rows   = len(self.maze_layout)
        self.maze_cols   = len(self.maze_layout[0])

        self.matrix        = self._load_wall_matrix()
        self.total_tablets = self._count_tablets()

        self.wall_surface = self._create_wall_surface()

    def _load_maze_layout (self, maze_file: str) -> list[list[int]]:
        """ Carrega o layout de desenho do labirinto. """
        maze = []
        with open(maze_file, 'r') as f:
            for line in f:
                row = [int(x) for x in line.split()]
                maze.append(row)
        return maze
    
    def _load_wall_matrix (self) -> list[list[int]]:
        """ Cria a matriz de colisão e pastilhas (-1=parede, 0=vazio, 1=pastilha, 2=powerup). """
        matrix = []
        for row in self.maze_layout:
            new_row = [-1 if x > 2 else x for x in row]
            matrix.append(new_row)
        return matrix
    
    def _count_tablets (self) -> int:
        count = 0
        for row in range(self.maze_rows):
            for col in range(self.maze_cols):
                if self.matrix[row][col] == 1 or self.matrix[row][col] == 2:
                    count += 1
        return count
    
    def _create_wall_surface (self) -> pygame.Surface:
        """ Desenha todas as paredes estáticas em uma Surface para otimização. """
        surface = pygame.Surface((self.maze_cols * self.cell_width, self.maze_rows * self.cell_height))
        surface.set_colorkey('black')

        color = self.wall_color

        for row in range(self.maze_rows):
            for col in range(self.maze_cols):
                x, y = col * self.cell_width, row * self.cell_height
                cell_code = self.maze_layout[row][col]

                if cell_code == 3:
                    x += self.cell_height // 2
                    pygame.draw.line(surface, color, (x, y), (x, y + self.cell_height))

                elif cell_code == 4:
                    y += self.cell_width // 2
                    pygame.draw.line(surface, color, (x, y), (x + self.cell_height, y))

                elif cell_code == 5:
                    x -= self.cell_height // 2
                    y += self.cell_width // 2
                    pygame.draw.arc(surface, color, (x, y, self.cell_height, self.cell_width), 0, math.pi / 2)

                elif cell_code == 6:
                    x += self.cell_height // 2
                    y += self.cell_width // 2
                    pygame.draw.arc(surface, color, (x, y, self.cell_height, self.cell_width), math.pi / 2, math.pi)

                elif cell_code == 7:
                    x += self.cell_height // 2
                    y -= self.cell_width // 2
                    pygame.draw.arc(surface, color, (x, y, self.cell_height, self.cell_width), math.pi, 3 * math.pi / 2)

                elif cell_code == 8:
                    x -= self.cell_height // 2
                    y -= self.cell_width // 2
                    pygame.draw.arc(surface, color, (x, y, self.cell_height, self.cell_width), 3 * math.pi / 2, 2 * math.pi)

                elif cell_code == 9:
                    y += self.cell_width // 2
                    pygame.draw.line(surface, "white", (x, y), (x + self.cell_height, y))

        return surface
    
    def draw_walls (self, screen):
        """ Desenha as paredes (que já estão pré-renderizadas). """
        screen.blit(self.wall_surface, (0, 0))

    def draw_tablets (self, screen):
        """ Desenha as pastilhas. """
        color = 'white'

        for row in range(self.maze_rows):
            for col in range(self.maze_cols):
                x, y = col * self.cell_width, row * self.cell_height

                if self.matrix[row][col] == 1:
                    x += self.cell_height // 2
                    y += self.cell_width // 2
                    pygame.draw.circle(screen, color, (x, y), 2)

                if self.matrix[row][col] == 2:
                    x += self.cell_height // 2
                    y += self.cell_width // 2
                    pygame.draw.circle(screen, color, (x, y), 6)