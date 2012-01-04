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
	if self.steps_to_fight == 0:
	    self.steps_to_fight = self.generate_steps_to_fight()
	    return True

	if 'fight' in tile:
	    return tile['fight']

	return False

    def input(self, pygame_event, frame_num):
        if pygame_event.type != pygame.KEYDOWN:
            return

        key = pygame_event.dict['key']
        if key in [273, 274]:
            self.current_fight._fight_menu.move_selection(key, frame_num)
            return None

        if key == 122:
            action = self.current_fight._fight_menu.selected()
            self.current_fight.attack(frame_num)
            return None

        if key == 120:
            return 'fight_over'

        return None

    def generate_fight(self, screen, frame_num):
	sounds.play_random_battle_song()
        self.current_fight = Fight(screen, frame_num)

    def draw_combat(self, screen, frame_num):
        self.current_fight.draw(screen, frame_num)


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
    def __init__(self, screen, frame_num):
        self._start_frame = frame_num
        self._center = (screen.width / 2, screen.height / 2)

        self._enemies = [enemies.Karon()]

        seconds_for_opener = 0.5
        self.state = OPENER
        self.state_start = frame_num
        self.state_duration = seconds_for_opener * tiled_screen.FPS

        self._fight_menu = menu.FightMenu(frame_num)
        self._sound_channel = sounds.get_channel()

    def draw(self, screen, frame_num):
        state_perc = (1.0 * frame_num - self.state_start) / self.state_duration
        if self.state == OPENER:
            self.draw_opener(screen, state_perc)
            if state_perc > 1:
                self.state = INPUT
                for enemy in self._enemies:
                    enemy.blit(screen.screen)

        elif self.state == INPUT:
            self._fight_menu.blit_menu(screen.screen, frame_num)
        elif self.state == ATTACK:
            self.draw_attack(screen, frame_num)
        elif self.state == ATTACK_RESULT:
            self.draw_attack_result(screen, frame_num)
        elif self.state == SPELL:
            pass
        elif self.state == ENEMIES:
            self.state = INPUT

    def draw_opener(self, screen, opener_perc):
        box_size = (screen.width * opener_perc, screen.height * opener_perc)
        box_start_point = (self._center[0] * (1 - opener_perc),
                           self._center[1] * (1 - opener_perc))

        screen.screen.fill(black, (box_start_point + box_size))

    def draw_attack(self, screen, frame_num):
        self._fight_menu.hide(screen.screen)
        if self._sound_channel.get_busy():
            return

        self.attack_result(frame_num)

    def draw_attack_result(self, screen, frame_num):
        if self._sound_channel.get_busy():
            if self._attack_result == MISS:
                return

            to_blit = ((frame_num - self.state_start) / 5) % 2
            if to_blit:
                self._enemies[0].blit(screen.screen)
            else:
                self._enemies[0].hide(screen.screen)

            return

        if True:
            #last attacker
            self.state = ENEMIES
            for enemy in self._enemies:
                enemy.blit(screen.screen)

    def attack(self, frame_num):
        self.state = ATTACK
        self.state_start = frame_num

        self._sound_channel.queue(sounds.attack_sound)

    def attack_result(self, frame_num):
        self.state = ATTACK_RESULT
        self.state_start = frame_num

        rand = random.random()
        if rand > 0.5:
            self._attack_result = HIT
            self.state_duration = 0.5 * tiled_screen.FPS
            self._sound_channel.queue(sounds.hit_sound)
        elif rand > 0.25:
            self._attack_result = CRIT
            self.state_duration = 0.5 * tiled_screen.FPS
            self._sound_channel.queue(sounds.critical_sound)
        else:
            self._attack_result = MISS
            self.state_duration = 0.4 * tiled_screen.FPS
            self._sound_channel.queue(sounds.dodge_sound)
