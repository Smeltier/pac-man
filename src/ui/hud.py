import pygame

class HUD:

    _text_font_size: int
    _game_over_font_size: int
    _score_color: str
    _lives_color: str
    _game_over_color: str
    _victory_color: str
    _padding: int
    _screen: pygame.Surface
    _screen_width: int
    _screen_height: int
    _text_font: pygame.font.Font
    _game_over_font: pygame.font.Font

    def __init__(self, screen: pygame.Surface, config: dict):
        font_config: dict = config.get("font_size", {})
        self._text_font_size = font_config.get("text_font", 36)
        self._game_over_font_size = font_config.get("game_over", 72)

        color_config: dict = config.get("text_color", {})
        self._score_color = color_config.get("score", "white")
        self._lives_color = color_config.get("lives", "yellow")
        self._game_over_color = color_config.get("game_over", "red")
        self._victory_color = color_config.get("victory", "green")
        
        self._padding = config.get("padding", 10)
        
        self._screen = screen
        self._screen_width = screen.get_width()
        self._screen_height = screen.get_height()

        self._initialize_fonts()

    def draw_score(self, score: int, lives: int):
        self._draw_score_text(score)
        self._draw_lives_text(lives)

    def draw_game_over(self):
        self._draw_centered_message("GAME OVER", self._game_over_color)

    def draw_victory(self):
        self._draw_centered_message("YOU WIN!", self._victory_color)

    def _initialize_fonts(self):
        try:
            self._text_font = pygame.font.Font(None, self._text_font_size)
            self._game_over_font = pygame.font.Font(None, self._game_over_font_size) 
        except IOError:
            default_font = pygame.font.get_default_font()
            self._text_font = pygame.font.SysFont(default_font, self._text_font_size)
            self._game_over_font = pygame.font.SysFont(default_font, self._game_over_font_size)

    def _draw_score_text(self, score: int):
        text_surface = self._text_font.render(f"SCORE: {score}", True, self._score_color)
        text_rect = text_surface.get_rect(topleft=(self._padding, self._padding))
        self._screen.blit(text_surface, text_rect)

    def _draw_lives_text(self, lives: int):
        lives_surface = self._text_font.render(f"LIVES: {lives}", True, self._lives_color)
        lives_rect = lives_surface.get_rect(topright=(self._screen_width - self._padding, self._padding))
        self._screen.blit(lives_surface, lives_rect)

    def _draw_centered_message(self, message: str, color: str):
        text_surface = self._game_over_font.render(message, True, color)
        text_rect = text_surface.get_rect(center=(self._screen_width // 2, self._screen_height // 2))
        self._screen.blit(text_surface, text_rect)