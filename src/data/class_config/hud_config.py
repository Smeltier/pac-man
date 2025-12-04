from src.core.settings import Settings

class HUDConfig ():

    def __init__ (self, settings: Settings) -> None:
        config = Settings.get("hud", {})
        font_size_config = config.get("font_size", {})
        text_color_config = config.get("text_color", {})

        self.TEXT_FONT_SIZE = font_size_config.get("text_font", 1)
        self.GAME_OVER_FONT_SIZE = font_size_config.get("game_over", 1)
        self.SCORE_COLOR = text_color_config.get("score", "black")
        self.LIVES_COLOR = text_color_config.get("lives", "black")
        self.GAME_OVER_COLOR = text_color_config.get("game_over", "black")
        self.VICTORY_COLOR = text_color_config.get("victory", "black")
        self.PADDING = config.get("padding", 1)