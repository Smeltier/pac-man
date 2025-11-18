import pygame

class HUD ():

    def __init__(self, screen):
        self.screen = screen

        try:
            self.text_font = pygame.font.Font(None, 36)
        except IOError:
            print("Fonte padrão não encontrada, usando fonte de sistema.")
            self.text_font = pygame.font.SysFont(pygame.font.get_default_font(), 36)

    def draw_score(self, score):
        """ Desenha o placar do jogo baseado na pontuação do Pac-Man. """

        text_surface = self.text_font.render(f"SCORE: {score}", True, 'white')
        text_rect = text_surface.get_rect(topleft = (10, 10))
        self.screen.blit(text_surface, text_rect)