import pygame

from src.data.class_config.hud_config import HUDConfig

class HUD ():

    def __init__(self, screen, hud_config: HUDConfig):

        self.TEXT_FONT_SIZE = hud_config.TEXT_FONT_SIZE
        self.GAME_OVER_FONT_SIZE = hud_config.GAME_OVER_FONT_SIZE
        self.SCORE_COLOR = hud_config.SCORE_COLOR
        self.LIVES_COLOR = hud_config.LIVES_COLOR
        self.GAME_OVER_COLOR = hud_config.GAME_OVER_COLOR
        self.VICTORY_COLOR = hud_config.VICTORY_COLOR
        self.PADDING = hud_config.PADDING
        
        self._screen = screen
        self._screen_width = screen.get_width()
        self._screen_height = screen.get_height()

        try:
            self._text_font = pygame.font.Font(None, self.TEXT_FONT_SIZE)
            self._game_over_font = pygame.font.Font(None, self.GAME_OVER_FONT_SIZE) 
        except IOError:
            self._text_font = pygame.font.SysFont(pygame.font.get_default_font(), self.TEXT_FONT_SIZE)
            self._game_over_font = pygame.font.SysFont(pygame.font.get_default_font(), self.GAME_OVER_FONT_SIZE)

    def draw_score(self, score, lives):
        self._draw_score_text(score)
        self._draw_lives_text(lives)

    def draw_game_over(self):
        self._draw_centered_message("GAME OVER", self.GAME_OVER_COLOR)

    def draw_victory(self):
        self._draw_centered_message("YOU WIN!", self.VICTORY_COLOR)

    def _draw_score_text(self, score):
        text_surface = self._text_font.render(f"SCORE: {score}", True, self.SCORE_COLOR)
        text_rect = text_surface.get_rect(topleft = (self.PADDING, self.PADDING))
        self._screen.blit(text_surface, text_rect)

    def _draw_lives_text(self, lives):
        lives_surface = self._text_font.render(f"LIVES: {lives}", True, self.LIVES_COLOR)
        lives_rect = lives_surface.get_rect(topright = (self._screen_width - self.PADDING, self.PADDING))
        self._screen.blit(lives_surface, lives_rect)

    def _draw_centered_message(self, message, color):
        text_surface = self._game_over_font.render(message, True, color)
        text_rect = text_surface.get_rect(center = (self._screen_width // 2, self._screen_height // 2))
        self._screen.blit(text_surface, text_rect)