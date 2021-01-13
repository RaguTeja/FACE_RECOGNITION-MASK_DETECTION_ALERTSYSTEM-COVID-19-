from pygame import mixer

class SoundAlert:

    mixer.init()                              # intitializing our mixer for beep

    def sound_alert(self):
        sound = mixer.Sound('bb.wav')         # passed our required audio sound beep
        sound.play()                          # playing the sound


