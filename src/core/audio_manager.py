import pygame

from src.core.settings import Settings

class AudioManager ():

    MUSIC_VOLUME = 0.2
    WAKA_VOLUME = 0.4 
    
    SIREN_CHASE_PATH = 'src/data/sounds/siren_background_sound.wav'
    SIREN_VULNERABLE_PATH = 'src/data/sounds/power_up_sound.wav'
    WAKA_WAKA_PATH = 'src/sounds/waka_waka.wav'

    def __init__ (self) -> None:

        self._initial_config()
        
        self._siren_chase_path = self.SIREN_CHASE_PATH
        self._siren_vulnerable_path = self.SIREN_VULNERABLE_PATH

        try:
            self._eat_sound = pygame.mixer.Sound(self.WAKA_WAKA_PATH)
            self._eat_sound.set_volume(self.WAKA_VOLUME)
        except pygame.error as e:
            print(f"Erro ao carregar 'Waka Waka.wav': {e}")
            self._eat_sound = None

        pygame.mixer.music.set_volume(self.MUSIC_VOLUME)

    def play_chase (self) -> None:
        self._play_music(self._siren_chase_path)

    def play_vulnerable (self) -> None:
        self._play_music(self._siren_vulnerable_path)

    def play_waka(self) -> None:
        if not self._eat_sound: return 
        
        if self._eat_sound.get_num_channels() == 0:
            self._eat_sound.play(loops=-1)
    
    def stop_waka (self) -> None:
        if self._eat_sound:
            self._eat_sound.stop()

    def _play_music (self, path) -> None:
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(loops = -1)
        except pygame.error as e:
            print(f"Erro ao carregar música: {e}")