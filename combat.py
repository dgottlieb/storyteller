import pygame

import enemies
import menu
import random
import sounds
import tiled_screen

white = (255, 255, 255)
black = (0, 0, 0)

class CombatManager(object):
    def __init__(self, average_steps_to_fight, deviation):
	self.average_steps_to_fight = average_steps_to_fight
	self.deviation = deviation

	self.steps_to_fight = self.generate_steps_to_fight()
        self.current_fight = None

    def generate_steps_to_fight(self):
	return int(random.normalvariate(self.average_steps_to_fight, self.deviation))

    def step(self, tile):
	self.steps_to_fight -= 1
	if 'exit' in tile:
	    return False

	if self.steps_to_fight == 0:
	    self.steps_to_fight = self.generate_steps_to_fight()
	    return True

	if 'fight' in tile:
	    return tile['fight']

	return False

    def input(self, pygame_event, time):
        if pygame_event.type != pygame.KEYDOWN:
            return

        if self.current_fight.state != INPUT:
            return

        key = pygame_event.dict['key']
        if key in [273, 274]:
            self.current_fight._fight_menu.move_selection(key, time)
            return None

        if key == 122:
            action = self.current_fight._fight_menu.selected()
            if action == 'attack':
                self.current_fight.attack(time)

            return None

        if key == 120:
            return 'fight_over'

        return None

    def generate_fight(self, screen, time):
	sounds.play_random_battle_song()
        self.current_fight = Fight(screen, time)

    def draw_combat(self, screen, time):
        self.current_fight.draw(screen, time)


OPENER = 0
INPUT = 1
ATTACK = 2
SPELL = 3
ENEMIES = 4
ATTACK_RESULT = 5
SPELL_RESULT = 6

HIT = 0
CRIT = 1
MISS = 2

class Fight(object):
    def __init__(self, screen, start_time):
        self._start_time = start_time
        self._center = (screen.width / 2, screen.height / 2)

        if random.random() > 0.5:
            self._enemies = [enemies.Karon()]
        else:
            self._enemies = [enemies.Karon()] * 2

        seconds_for_opener = 0.5
        self.state = OPENER
        self.state_start = start_time
        self.state_duration = seconds_for_opener

        self._fight_menu = menu.FightMenu(start_time)
        self._sound_channel = sounds.get_channel()

        self.attacked_enemy_pos = -1

    def draw(self, screen, time):
        state_perc = (1.0 * time - self.state_start) / self.state_duration / 1000
        if self.state == OPENER:
            self.draw_opener(screen, state_perc)
            if state_perc > 1:
                self.state = INPUT
                for idx in range(len(self._enemies)):
                    enemy = self._enemies[idx]
                    enemy.blit(screen.screen, idx, len(self._enemies))

        elif self.state == INPUT:
            self._fight_menu.blit_menu(screen.screen, time)
        elif self.state == ATTACK:
            self.draw_attack(screen, time)
        elif self.state == ATTACK_RESULT:
            self.draw_attack_result(screen, time)
        elif self.state == SPELL:
            pass
        elif self.state == ENEMIES:
            self.state = INPUT

    def draw_opener(self, screen, opener_perc):
        box_size = (screen.width * opener_perc, screen.height * opener_perc)
        box_start_point = (self._center[0] * (1 - opener_perc),
                           self._center[1] * (1 - opener_perc))

        screen.screen.fill(black, (box_start_point + box_size))

    def draw_attack(self, screen, time):
        self._fight_menu.hide(screen.screen)
        if self._sound_channel.get_busy():
            return

        self.attack_result(time)

    def draw_attack_result(self, screen, time):
        if self._sound_channel.get_busy():
            if self._attack_result == MISS:
                return

            to_blit = (time - self.state_start) % 200 < 100
            if to_blit:
                self._enemies[0].blit(screen.screen, self.attacked_enemy_pos, len(self._enemies))
            else:
                self._enemies[0].hide(screen.screen, self.attacked_enemy_pos, len(self._enemies))

            return

        if True:
            #last attacker
            self.state = ENEMIES
            for idx in range(len(self._enemies)):
                enemy = self._enemies[idx]
                enemy.blit(screen.screen, idx, len(self._enemies))

    def attack(self, time):
        self.state = ATTACK
        self.state_start = time

        self.attacked_enemy_pos = random.choice(range(len(self._enemies)))

        self._sound_channel.queue(sounds.attack_sound)

    def attack_result(self, time):
        self.state = ATTACK_RESULT
        self.state_start = time

        rand = random.random()
        if rand > 0.5:
            self._attack_result = HIT
            self.state_duration = 0.5
            self._sound_channel.queue(sounds.hit_sound)
        elif rand > 0.25:
            self._attack_result = CRIT
            self.state_duration = 0.5
            self._sound_channel.queue(sounds.critical_sound)
        else:
            self._attack_result = MISS
            self.state_duration = 0.4
            self._sound_channel.queue(sounds.dodge_sound)
