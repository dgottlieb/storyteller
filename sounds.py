import pygame

import random

pygame.mixer.init(buffer=2**8)
pygame.mixer.music.set_volume(0.8)

bump_sound = pygame.mixer.Sound('./sounds/bump.wav')
bump_sound.set_volume(0.8)

stair_sound = pygame.mixer.Sound('./sounds/stairs.wav')
stair_sound.set_volume(0.8)

attack_sound = pygame.mixer.Sound('./sounds/attack.wav')
attack_sound.set_volume(0.8)

hit_sound = pygame.mixer.Sound('./sounds/hit.wav')
hit_sound.set_volume(0.8)

dodge_sound = pygame.mixer.Sound('./sounds/dodge.wav')
dodge_sound.set_volume(0.8)

critical_sound = pygame.mixer.Sound('./sounds/criticalhit.wav')
critical_sound.set_volume(0.8)

win_battle_sound = pygame.mixer.Sound('./sounds/winbattle.wav')
win_battle_sound.set_volume(0.8)

def play_music(song_file, loops=-1):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(song_file)
    pygame.mixer.music.play(loops)

def stop_music():
    pygame.mixer.music.stop()

beep_sound = pygame.mixer.Sound('./sounds/beep.wav')
beep_sound.set_volume(0.8)

battles = 0
#battle_songs_names = ['./sounds/dq%d-battle.mid' % (game_num,) for game_num in range(2, 7)]
battle_songs_names = ['./sounds/dq4-battle.mid']
random.shuffle(battle_songs_names)
def play_random_battle_song():
    global battles
    if battles == len(battle_songs_names):
	random.shuffle(battle_songs_names)
	battles = 0

    play_music(battle_songs_names[battles])
    battles += 1

def get_channel():
    for channel_id in range(pygame.mixer.get_num_channels()):
        channel = pygame.mixer.Channel(channel_id)
        if channel.get_busy() == False:
            return channel

    return None
