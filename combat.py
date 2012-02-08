import pygame

import enemies
import inform
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

    def input(self, screen, pygame_event, time):
        if pygame_event.type != pygame.KEYDOWN:
            return

        if self.current_fight.state not in [INPUT, ENEMY_SELECT, WIN]:
            return

        key = pygame_event.dict['key']
        if self.current_fight.state == WIN and key in [120, 122]:
            return 'fight_over'

        if key in [273, 274]:
            self.current_fight._menus[-1].move_selection(key, time)
            return None

        if key == 122:
            action = self.current_fight._menus[-1].selected()
            if action in ['attack', 'spell']:
                self.current_fight.generate_enemy_select_menu(time, action)

            if len(action) == 2:
                action_type, position = action
                if action_type == 'attack':
                    self.current_fight.attack(time, position)

            return None

        if key == 120:
            canceled_menu = self.current_fight._menus.pop()
            canceled_menu.hide(screen.screen)
            if not self.current_fight._menus:
                return 'fight_over'

        return None

    def generate_fight(self, screen, time, party):
	sounds.play_random_battle_song()
        self.current_fight = Fight(screen, time, party)

    def draw_combat(self, screen, time):
        self.current_fight.draw(screen, time)


OPENER = 0
INPUT = 1
ATTACK = 2
SPELL = 3
ENEMIES = 4
ATTACK_RESULT = 5
SPELL_RESULT = 6
ENEMY_SELECT = 7
WIN = 8

HIT = 0
CRIT = 1
MISS = 2

class Fight(object):
    def __init__(self, screen, start_time, party):
        self._start_time = start_time
        self._center = (screen.width / 2, screen.height / 2)

        if random.random() > 0.5:
            self._enemies = [enemies.Karon()]
        else:
            self._enemies = [enemies.Karon(), enemies.Karon()]

        seconds_for_opener = 0.5
        self.state = OPENER
        self.state_start = start_time
        self.state_duration = seconds_for_opener

        self._menus = [menu.FightMenu(start_time)]
        self._combat_log = inform.CombatLog()
        self._sound_channel = sounds.get_channel()

        self.attacked_enemy_pos = -1
        self.party = party
        self.active_pc_idx = 0

    def draw(self, screen, time):
        state_perc = (1.0 * time - self.state_start) / self.state_duration / 1000
        if self.state == OPENER:
            self.draw_opener(screen, state_perc)
            if state_perc > 1:
                self.state = INPUT
                for idx in range(len(self._enemies)):
                    enemy = self._enemies[idx]
                    enemy.blit(screen.screen, idx, len(self._enemies))

        elif self.state == INPUT or self.state == ENEMY_SELECT:
            self._menus[-1].blit_menu(screen.screen, time)
        elif self.state == ATTACK:
            self.draw_attack(screen, state_perc, time)
        elif self.state == ATTACK_RESULT:
            self.draw_attack_result(screen, state_perc, time)
        elif self.state == SPELL:
            self._combat_log.blit(screen.screen)
        elif self.state == ENEMIES:
            self._combat_log.hide(screen.screen)
            self._combat_log.clear()
            self.state = INPUT
        elif self.state == WIN:
            pass

    def draw_opener(self, screen, opener_perc):
        box_size = (screen.width * opener_perc, screen.height * opener_perc)
        box_start_point = (self._center[0] * (1 - opener_perc),
                           self._center[1] * (1 - opener_perc))

        screen.screen.fill(black, (box_start_point + box_size))

    def draw_attack(self, screen, state_perc, time):
        for menu in self._menus:
            menu.hide(screen.screen)

        self._combat_log.blit(screen.screen)

        if state_perc < 0.4:
            return

        if not self._combat_log.lines:
            self._combat_log.append(self._attack_log_line)
            self._attack_log_line = None
            self._sound_channel.queue(sounds.attack_sound)

        if self._sound_channel.get_busy():
            return

        if state_perc >= 1.0:
            self.attack_result(time)

    def draw_attack_result(self, screen, state_perc, time):
        self._combat_log.blit(screen.screen)

        if self._sound_channel.get_busy():
            if self._attack_result == MISS:
                return

            to_blit = (time - self.state_start) % 200 < 100
            if to_blit:
                self.attacked_enemy.blit(screen.screen, self.attacked_enemy_pos, len(self._enemies))
            else:
                self.attacked_enemy.hide(screen.screen, self.attacked_enemy_pos, len(self._enemies))

            return

        if state_perc < 1.0:
            return

        attack_menu = self._menus.pop()
        self.active_pc_idx += 1
        if self.active_pc_idx == len(self.party.members):
            #last attacker - enemies fight back
            self.active_pc_idx = 0
            self.state = ENEMIES
            for idx in range(len(self._enemies)):
                enemy = self._enemies[idx]
                enemy.blit_if_alive(screen.screen, idx, len(self._enemies))

        if self.is_over:
            self.state = WIN
            while self._menus:
                popped_menu = self._menus.pop()
                popped_menu.hide(screen.screen)

            sounds.stop_music()
            sounds.win_battle_sound.play()

            self._combat_log.clear()
            self._combat_log.append("You have vanquished the enemies!")
            self._combat_log.append("You received 0 gold and 0 exp, loser.")
            self._combat_log.append("(But you walk away with your life.)")
            self._combat_log.blit(screen.screen)

            
    def attack(self, time, enemy_pos):
        self.state = ATTACK
        self.state_start = time

        for enemy in self._enemies[:enemy_pos+1]:
            if enemy.alive == False:
                enemy_pos += 1

        self.attacked_enemy_pos = enemy_pos
        self._attack_log_line = "You attack %s" % (self._enemies[enemy_pos].name,)

    def attack_result(self, time):
        self.state = ATTACK_RESULT
        self.state_start = time

        self.attacked_enemy = self._enemies[self.attacked_enemy_pos]
        attacker = self.party.members[self.active_pc_idx]
        result = attacker.melee(self.attacked_enemy)
        self._combat_log.append(result["feedback"])

        if result["action"] == 'hit':
            self._attack_result = HIT
            self.state_duration = 1.0
            self._sound_channel.queue(sounds.hit_sound)
        elif result["action"] == 'crit':
            self._attack_result = CRIT
            self.state_duration = 1.0
            self._sound_channel.queue(sounds.critical_sound)
        elif result["action"] == 'miss':
            self._attack_result = MISS
            self.state_duration = 0.8
            self._sound_channel.queue(sounds.dodge_sound)

    def generate_enemy_select_menu(self, time, action_type):
        self._menus.append(EnemySelectionMenu(time, self._enemies, action_type))

    @property
    def is_over(self):
        return all(map(lambda x: x.alive == False, self._enemies))

class EnemySelectionMenu(menu.BaseMenu):
    def __init__(self, start_time, enemies, action_type):
        menu_items = [(enemy.menu_option(),) for enemy in enemies if enemy.alive]
        menu.BaseMenu.__init__(self, start_time, (100, 350), menu_items)
        self.action_type = action_type

    def selected(self):
        position = self.selection[0]
        return self.action_type, position
