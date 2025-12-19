import pygame

class AudioManager:

    _music_volume: float
    _waka_volume: float
    _siren_chase_path: str
    _siren_vulnerable_path: str
    _waka_path: str
    _eat_sound: pygame.mixer.Sound

    def __init__(self, config: dict) -> None:
        constants_config: dict = config.get("constants", {})
        self._music_volume = constants_config.get("music_volume", 0.2)
        self._waka_volume = constants_config.get("waka_volume", 0.4)

        paths_config: dict = config.get("paths", {})
        self._siren_chase_path = paths_config.get("siren_chase", "")
        self._siren_vulnerable_path = paths_config.get("siren_vulnerable", "")
        self._waka_path = paths_config.get("waka_path", "")
        
        self._eat_sound = None
        
        if self._waka_path:
            try:
                self._eat_sound = pygame.mixer.Sound(self._waka_path)
                self._eat_sound.set_volume(self._waka_volume)
            except pygame.error as e:
                print(f"Erro ao carregar '{self._waka_path}': {e}")

        try:
            pygame.mixer.music.set_volume(self._music_volume)
        except pygame.error:
             pass

    def play_chase(self) -> None:
        if self._siren_chase_path:
            self._play_music(self._siren_chase_path)

    def play_vulnerable(self) -> None:
        if self._siren_vulnerable_path:
            self._play_music(self._siren_vulnerable_path)

    def play_waka(self) -> None:
        if not self._eat_sound: 
            return 
        
        if self._eat_sound.get_num_channels() == 0:
            self._eat_sound.play(loops=-1)
    
    def stop_waka(self) -> None:
        if self._eat_sound:
            self._eat_sound.stop()

    def _play_music(self, path: str) -> None:
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(loops=-1)
        except pygame.error as e:
            print(f"Erro ao carregar música '{path}': {e}")