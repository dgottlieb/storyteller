import pygame

pygame.mixer.init()
pygame.mixer.music.set_volume(0.8)

bump_sound = pygame.mixer.Sound('./sounds/bump.wav')
bump_sound.set_volume(0.8)

stair_sound = pygame.mixer.Sound('./sounds/stairs.wav')
stair_sound.set_volume(0.8)


def play_music(song_file):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(song_file)
    pygame.mixer.music.play(-1)
