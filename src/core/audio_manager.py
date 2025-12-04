import pygame

from src.data.class_config.audio_manager_config import AudioManagerConfig

class AudioManager ():

    def __init__ (self, audio_manager_config: AudioManagerConfig) -> None:

        self.MUSIC_VOLUME = audio_manager_config.MUSIC_VOLUME
        self.WAKA_VOLUME = audio_manager_config.WAKA_VOLUME
        self.SIREN_CHASE_PATH = audio_manager_config.SIREN_CHASE_PATH
        self.SIREN_VULNERABLE_PATH = audio_manager_config.SIREN_VULNERABLE_PATH
        self.WAKA_WAKA_PATH = audio_manager_config.WAKA_WAKA_PATH
        
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