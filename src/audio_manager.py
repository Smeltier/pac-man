import pygame

class AudioManager ():

    def __init__ (self):
        self._siren_chase_path = 'src/sounds/siren_background_sound.wav'
        self._siren_vulnerable_path = 'src/sounds/power_up_sound.wav'

        try:
            self.eat_sound = pygame.mixer.Sound('src/sounds/waka_waka.wav')
            self.eat_sound.set_volume(0.4)
        except pygame.error as e:
            print(f"Erro ao carregar 'Waka Waka.wav': {e}")
            self.eat_sound = None

        pygame.mixer.music.set_volume(0.2)

    def play_chase (self):
        try:
            pygame.mixer.music.load(self._siren_chase_path)
            pygame.mixer.music.play(loops = -1)
        except pygame.error as e:
            print(f"Erro ao carregar música de perseguição: {e}")

    def play_vulnerable (self):
        try:
            pygame.mixer.music.load(self._siren_vulnerable_path)
            pygame.mixer.music.play(loops = -1)
        except pygame.error as e:
            print(f"Erro ao carregar música de perseguição: {e}")

    def play_waka(self):
        """ Toca o som de comer, se ainda não estiver tocando. """
        if not self.eat_sound: return 
        
        if self.eat_sound.get_num_channels() == 0:
            self.eat_sound.play(loops=-1)
    
    def stop_waka(self):
        """ Para o som de comer. """
        if self.eat_sound:
            self.eat_sound.stop()