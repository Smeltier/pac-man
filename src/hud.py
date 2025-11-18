import pygame

class HUD ():

    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()

        try:
            self.text_font = pygame.font.Font(None, 36)
            self.game_over_font = pygame.font.Font(None, 72) 
        except IOError:
            print("Fonte padrão não encontrada, usando fonte de sistema.")
            self.text_font = pygame.font.SysFont(pygame.font.get_default_font(), 36)
            self.game_over_font = pygame.font.SysFont(pygame.font.get_default_font(), 72)

    def draw_score(self, score, lives):
        text_surface = self.text_font.render(f"SCORE: {score}", True, 'white')
        text_rect = text_surface.get_rect(topleft = (10, 10))
        self.screen.blit(text_surface, text_rect)

        lives_surface = self.text_font.render(f"LIVES: {lives}", True, 'yellow')
        lives_rect = lives_surface.get_rect(topright = (self.width - 10, 10))
        self.screen.blit(lives_surface, lives_rect)

    def draw_game_over(self):
        text_surface = self.game_over_font.render("GAME OVER", True, 'red')
        text_rect = text_surface.get_rect(center = (self.width // 2, self.height // 2))
        self.screen.blit(text_surface, text_rect)

    def draw_victory(self):
        text_surface = self.game_over_font.render("YOU WIN!", True, 'green')
        text_rect = text_surface.get_rect(center = (self.width // 2, self.height // 2))
        self.screen.blit(text_surface, text_rect)