import pygame

from src.hud import HUD
from src.maze import Maze
from src.states import GameState, GhostState
from src.audio_manager import AudioManager

class Environment ():

    def __init__ (self, screen, maze_file: str):
        self.screen = screen

        self.game_state = GameState.CHASE
        self.entities = []
        self.lives = 3

        self.vulnerable_timer    = 0
        self.vulnerable_duration = 7000
        self.scatter_time = pygame.time.get_ticks()
        self.current_global_mode = GhostState.SCATTER
        self.chase_time = 20000
        self.scatter_time = 7000

        self.game_over_start_time = 0
        self.game_over_duration = 4000 

        cell_width  = screen.get_width() // 30
        cell_height = screen.get_height() // 32

        self.maze = Maze(maze_file, cell_width, cell_height)
        self.hud  = HUD(screen)
        self.audio_manager = AudioManager()

        self.matrix = self.maze.matrix
        self.cell_width = self.maze.cell_width
        self.cell_height = self.maze.cell_height

        self.audio_manager.play_chase()

    def add_entity (self, entity) -> None:
        if entity is None:
            raise ValueError('Entidade inválida.')

        if entity not in self.entities:
            self.entities.append(entity)
    
    def remove_entity (self, entity) -> None:
        self.entities = [e for e in self.entities if e is not entity]

    def set_vulnerable (self) -> None:
        if self.game_state == GameState.CHASE:
            self.game_state = GameState.VULNERABLE
            self.audio_manager.play_vulnerable()
            self.vulnerable_timer = pygame.time.get_ticks()
    
    def set_chase (self) -> None:
        self.game_state = GameState.CHASE
        self.audio_manager.play_chase()

    def get_global_ghost_mode (self) -> GhostState:
        now = pygame.time.get_ticks()

        if self.current_global_mode == GhostState.SCATTER:
            if now - self.scatter_time > self.scatter_time:
                self.current_global_mode = GhostState.CHASE
                self.scatter_time = now
        else:
            if now - self.scatter_time > self.chase_time:
                self.current_global_mode = GhostState.SCATTER
                self.scatter_time = now

        return self.current_global_mode
    
    def handle_player_death(self):
        self.lives -= 1

        if self.lives > 0:
            self.reset_level()
        else:
            self.game_state = GameState.GAME_OVER
            self.game_over_start_time = pygame.time.get_ticks()

    def handle_victory(self):
        """ Chamado quando o jogador come todas as pastilhas. """
        self.game_state = GameState.VICTORY
        
        self.audio_manager.stop_waka() 
        pygame.mixer.music.stop() 
        
        self.game_over_start_time = pygame.time.get_ticks()
    
    def reset_level(self):
        pygame.time.delay(1000) 
        self.set_chase()
        self.scatter_timer = pygame.time.get_ticks()
        self.current_global_mode = GhostState.SCATTER

        for entity in self.entities:
            if hasattr(entity, 'reset'):
                entity.reset()

    def draw (self) -> None:
        self.screen.fill('black')
        
        self.maze.draw_walls(self.screen)
        self.maze.draw_tablets(self.screen)
        
        for entity in self.entities:
            entity.draw(self.screen)
            
        if self.entities:
            player_score = self.entities[0].total_points
            self.hud.draw_score(player_score, self.lives)
        
        if self.game_state == GameState.GAME_OVER:
            self.hud.draw_game_over()
        
        if self.game_state == GameState.VICTORY:
            self.hud.draw_victory()

    def update(self, delta_time: float) -> None:
        if self.game_state in [GameState.GAME_OVER, GameState.VICTORY]:
            now = pygame.time.get_ticks()
            if now - self.game_over_start_time > self.game_over_duration:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            return 

        if self.game_state == GameState.VULNERABLE:
            now = pygame.time.get_ticks()
            if now - self.vulnerable_timer > self.vulnerable_duration:
                self.set_chase()
        
        for entity in self.entities[:]:
            entity.update(delta_time)