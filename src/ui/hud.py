import pygame

class HUD ():

    TEXT_FONT_SIZE = 36
    GAME_OVER_FONT_SIZE = 72
    SCORE_COLOR = 'white'
    LIVES_COLOR = 'yellow'
    GAME_OVER_COLOR = 'red'
    VICTORY_COLOR = 'green'
    PADDING = 10

    def __init__(self, screen):
        
        self._screen = screen
        self._screen_width = screen.get_width()
        self._screen_height = screen.get_height()

        try:
            self._text_font = pygame.font.Font(None, self.TEXT_FONT_SIZE)
            self._game_over_font = pygame.font.Font(None, self.GAME_OVER_FONT_SIZE) 
        except IOError:
            self._text_font = pygame.font.SysFont(pygame.font.get_default_font(), self.TEXT_FONT_SIZE)
            self._game_over_font = pygame.font.SysFont(pygame.font.get_default_font(), self.GAME_OVER_FONT_SIZE)

    # MÉTODOS PÚBLICOS

    def draw_score(self, score, lives):
        self._draw_score_text(score)
        self._draw_lives_text(lives)

    def draw_game_over(self):
        self._draw_centered_message("GAME OVER", self.GAME_OVER_COLOR)

    def draw_victory(self):
        self._draw_centered_message("YOU WIN!", self.VICTORY_COLOR)

    # MÉTODOS PRIVADOS

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