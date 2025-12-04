from src.core.settings import Settings

class AudioManagerConfig ():

    def __init__ (self, settings: Settings) -> None:
        config: dict = settings.get("audio_manager", {})
        constrants_config: dict = config.get("constrants", {})
        paths_config: dict = config.get("paths", {})

        self.MUSIC_VOLUME = constrants_config.get("music_volume", 0.1)
        self.WAKA_VOLUME = constrants_config.get("waka_volume", 0.1)
        self.SIREN_CHASE_PATH = paths_config.get("siren_chase", "")
        self.SIREN_VULNERABLE_PATH = paths_config.get("siren_vulnerable", "")
        self.WAKA_WAKA_PATH = paths_config.get("waka_path", "")