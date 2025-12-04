from src.core.settings import Settings

class AudioManagerConfig ():

    def __init__ (self, settings: Settings) -> None:
        config = Settings.get("audio_manager")

        constrants_config = config.get("constrants")

        self.MUSIC_VOLUME = constrants_config.get("music_volume")
        self.WAKA_VOLUME = constrants_config.get("waka_volume")

        paths_config = config.get("paths")

        self.SIREN_CHASE_PATH = paths_config.get("siren_chase")
        self.SIREN_VULNERABLE_PATH = paths_config.get("siren_vulnerable")
        self.WAKA_WAKA_PATH = paths_config.get("waka_path")