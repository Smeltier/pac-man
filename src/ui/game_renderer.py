import pygame

from src.core.states import GameState

class GameRenderer:
    
    def __init__(self, screen: pygame.Surface):
        self._screen = screen

    def render(self, maze, entities, hud, game_state, score, lives):
        self._screen.fill('black')
        self._screen.blit(maze.wall_surface, (0, 0))

        self._draw_pellets(maze)
        
        for entity in entities:
            entity.draw(self._screen)
            
        hud.draw_score(score, lives)
        
        if game_state == GameState.GAME_OVER:
            hud.draw_game_over()
        elif game_state == GameState.VICTORY:
            hud.draw_victory()

    def _draw_pellets(self, maze):
        for row in range(maze.rows):
            for col in range(maze.cols):
                val = maze.matrix[row][col]

                if val == 1 or val == 2:
                    x = col * maze.cell_width + maze.cell_width // 2
                    y = row * maze.cell_height + maze.cell_height // 2
                    
                    if val == 1:
                        pygame.draw.circle(self._screen, maze.small_pellet_color, (x, y), maze.small_pellet_radius)
                    else:
                        pygame.draw.circle(self._screen, maze.power_pellet_color, (x, y), maze.power_pellet_radius)