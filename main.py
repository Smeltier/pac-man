from src.core.game import Game

pacman_game = Game(width = 900, height = 950, fps = 60)
pacman_game.run('data/settings/config.json')