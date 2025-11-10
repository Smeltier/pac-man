import math
import pygame

class Environment ():
    def __init__(self, screen, maze_file: str) -> None:
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.text_font = pygame.font.Font(None, 36)
        self.game_state = 'chase'
        self.vulnerable_timer = 0
        self.vulnerable_duration = 7000
        self.wall_color = 'blue'
        self.cell_width = self.width // 30
        self.cell_height = self.height // 32
        self.entities = []
        self.maze = self._load_maze(maze_file)
        self.maze_rows = len(self.maze)
        self.maze_cols = len(self.maze[0])
        self.matrix = self._load_walls()
        self.total_tablets = self._count_tablets()
        self.maze_surface = pygame.Surface((self.width, self.height))
        self.maze_surface.fill('black')
        self._draw_maze(self.maze_surface)

        self.siren_chase_path = 'pacman_game/sounds/Siren Background Sound.wav'
        self.siren_vulnerable_path = 'pacman_game/sounds/Power Up Sound.wav'
        pygame.mixer.music.load(self.siren_chase_path)
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(loops=-1)

    def _load_maze(self, maze_file: str) -> list[list[int]]:
        """ Carrega um labirinto a partir de um arquivo .txt """

        maze = []
        with open(maze_file, 'r') as f:
            for line in f:
                row = [int(x) for x in line.split()]
                maze.append(row)
        return maze
    
    def _load_walls(self) -> list[list[int]]:
        """ Transforma o labirinto em uma matrix numérica mais simples, formada por -1, 0, 1 e 2. """

        matrix = []
        for row in self.maze:
            new_row = [-1 if x > 2 else x for x in row]
            matrix.append(new_row)
        return matrix
    
    def _count_tablets(self) -> int:
        """ Conta a quantidade de pastilhas presentes no labirinto. """

        count = 0
        for row in range(self.maze_rows):
            for col in range(self.maze_cols):
                if self.matrix[row][col] == 1 or self.matrix[row][col] == 2:
                    count += 1
        return count
    
    def _draw_maze(self, surface) -> None:
        """ Desenha as paredes do labirinto em `surface`. """

        color = 'blue'
        for row in range(self.maze_rows):
            for col in range(self.maze_cols):
                x, y = col * self.cell_width, row * self.cell_height

                if self.maze[row][col] == 3:
                    x += self.cell_height // 2
                    pygame.draw.line(surface, color, (x, y), (x, y + self.cell_height))

                elif self.maze[row][col] == 4:
                    y += self.cell_width // 2
                    pygame.draw.line(surface, color, (x, y), (x + self.cell_height, y))

                elif self.maze[row][col] == 5:
                    x -= self.cell_height // 2
                    y += self.cell_width // 2
                    pygame.draw.arc(surface, color, (x, y, self.cell_height, self.cell_width), 0, math.pi / 2)

                elif self.maze[row][col] == 6:
                    x += self.cell_height // 2
                    y += self.cell_width // 2
                    pygame.draw.arc(surface, color, (x, y, self.cell_height, self.cell_width), math.pi / 2, math.pi)

                elif self.maze[row][col] == 7:
                    x += self.cell_height // 2
                    y -= self.cell_width // 2
                    pygame.draw.arc(surface, color, (x, y, self.cell_height, self.cell_width), math.pi, 3 * math.pi / 2)

                elif self.maze[row][col] == 8:
                    x -= self.cell_height // 2
                    y -= self.cell_width // 2
                    pygame.draw.arc(surface, color, (x, y, self.cell_height, self.cell_width), 3 * math.pi / 2, 2 * math.pi)

                elif self.maze[row][col] == 9:
                    y += self.cell_width // 2
                    pygame.draw.line(surface, "white", (x, y), (x + self.cell_height, y))

    def _draw_tablets(self):
        """ Desenha as pastilhas. """

        color = 'white'
        for row in range(self.maze_rows):
            for col in range(self.maze_cols):
                x, y = col * self.cell_width, row * self.cell_height

                if self.matrix[row][col] == 1:
                    x += self.cell_height // 2
                    y += self.cell_width // 2
                    pygame.draw.circle(self.screen, color, (x, y), 2)

                if self.matrix[row][col] == 2:
                    x += self.cell_height // 2
                    y += self.cell_width // 2
                    pygame.draw.circle(self.screen, color, (x, y), 6)

    def _draw_entities(self) -> None:
        """ Desenha as entidades. """
        for entity in self.entities:
            entity.draw(self.screen)

    def _draw_score(self) -> None:
        """ Desenha o placar do jogador na tela. """

        if not self.entities: return

        player_score = self.entities[0].total_points
        text_surface = self.text_font.render(f"SCORE: {player_score}", True, 'white')
        text_rect = text_surface.get_rect(topleft=(10, 10))
        self.screen.blit(text_surface, text_rect)

    def draw(self) -> None:
        """ Desenha o ambiente e suas entidades. """

        self.screen.blit(self.maze_surface, (0, 0))
        self._draw_tablets()
        self._draw_entities()
        self._draw_score()

    def add_entity(self, entity) -> None:
        """ Adiciona uma nova entidade ao ambiente. """

        if entity is None: 
            raise ValueError('Entidade inválida.')
        if entity not in self.entities: 
            self.entities.append(entity)

    def remove_entity(self, entity) -> None:
        """ Remove uma entidade do ambiente. """
        self.entities = [e for e in self.entities if e is not entity]


    def set_vulnerable(self) -> None:
        """ Ativa o estado 'vulnerável' (fantasmas azuis). """
        
        if self.game_state == 'chase':
            self.game_state = 'vulnerable'
            pygame.mixer.music.load(self.siren_vulnerable_path)
            pygame.mixer.music.play(loops=-1)
            self.vulnerable_timer = pygame.time.get_ticks()

    def set_chase(self) -> None:
        """ Ativa o estado 'perseguição' (normal). """
        
        self.game_state = 'chase'
        pygame.mixer.music.load(self.siren_chase_path)
        pygame.mixer.music.play(loops=-1)

    def update(self, delta_time: float) -> None:
        """ Atualiza o ambiente e suas entidades de acordo com o passar do tempo. """

        if self.game_state == 'vulnerable':
            now = pygame.time.get_ticks()
            if now - self.vulnerable_timer > self.vulnerable_duration:
                self.set_chase()

        for entity in self.entities:
            entity.update(delta_time)