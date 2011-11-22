import spritesheet

chars_sheet = spritesheet.SpriteSheet("images/chars.png", background_color=(135, 191, 255, 255))

TPS = 2 #Twitches per second, characters transitioning between different states
MPS = 3 #Movement per second, how many tiles the hero can walk per second

def init_hero(screen):
    hero = [chars_sheet.get_item(1, x, 64, 64, transparent=True) for x in range(8)]
    screen.set_hero_down(hero[0:2])
    screen.set_hero_right(hero[2:4])
    screen.set_hero_left(hero[4:6])
    screen.set_hero_up(hero[6:8])
    screen.set_hero_tps(TPS)
    screen.set_walking_speed(MPS)
