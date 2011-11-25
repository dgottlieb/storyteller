import pygame

pygame.mixer.init(buffer=2**8)
pygame.mixer.music.set_volume(0.8)

bump_sound = pygame.mixer.Sound('./sounds/bump.wav')
bump_sound.set_volume(0.8)

stair_sound = pygame.mixer.Sound('./sounds/stairs.wav')
stair_sound.set_volume(0.8)

def play_music(song_file):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(song_file)
    pygame.mixer.music.play(-1)

beep_sound = pygame.mixer.Sound('./sounds/beep.wav')
beep_sound.set_volume(0.8)
