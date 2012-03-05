import pygame

import menu

import random

black = (0, 0, 0)
white = (255, 255, 255)

enemy_width = 125
enemy_height = 125

enemy_width_buffer = 25

class Enemy(object):
    def __init__(self, name, image_file, **kwargs):
        """Using kwargs because there are tons of bits that can be added. Current list:
        attack, defense, hit_points, gold, exp
        """
        raw_surface = pygame.image.load(image_file)
        self.surface = pygame.transform.scale(raw_surface, (enemy_width, enemy_height))
        self.name = name

        self.attack = kwargs.pop("attack", 0)
        self.defense = kwargs.pop("defense", 0)
        self.hit_points = kwargs.pop("hit_points", 1)

        self.initiative = kwargs.pop("initiative", 50)

        self.gold = kwargs.pop("gold", 0)
        self.exp = kwargs.pop("exp", 0)

    def blit_if_alive(self, screen, position, num_enemies):
        if not self.alive:
            self.hide(screen, position, num_enemies)
            return

        enemy_rectangle = self.enemy_rectangle(screen, position, num_enemies)
        screen.blit(self.surface, enemy_rectangle)

    def blit(self, screen, position, num_enemies):
        enemy_rectangle = self.enemy_rectangle(screen, position, num_enemies)
        screen.blit(self.surface, enemy_rectangle)

    def hide(self, screen, position, num_enemies):
        enemy_rectangle = self.enemy_rectangle(screen, position, num_enemies)
        screen.fill(black, enemy_rectangle)

    def enemy_rectangle(self, screen, position, num_enemies):
        fight_rectangle = self.fight_rectangle(screen)

        group_rectangle_relative = self.group_rectangle(num_enemies)
        group_rectangle_absolute = ((fight_rectangle[2] - group_rectangle_relative[0]) / 2 + 
                                    fight_rectangle[0],
                                    (fight_rectangle[3] - group_rectangle_relative[1]) / 2 +
                                    fight_rectangle[1],
                                    group_rectangle_relative[0], group_rectangle_relative[1])

        enemy_rectangle = (group_rectangle_absolute[0] + self.enemy_offset_from_left(position),
                           group_rectangle_absolute[1],
                           enemy_width, enemy_height)

        return enemy_rectangle

    def enemy_offset_from_left(self, position):
        return (enemy_width + enemy_width_buffer) * position

    def group_rectangle(self, num_enemies):
        rectangle_width = enemy_width * num_enemies + (enemy_width_buffer * (num_enemies - 1))
        return (rectangle_width, enemy_height)

    def fight_rectangle(self, screen):
        start_x = 100
        width = screen.get_width() - (2 * start_x)
        return (100, 150, width, 200)

    def menu_option(self):
        return menu.writer.render(self.name, menu.antialias, white, black)

    def attacked(self, damage):
        self.hit_points -= damage

    def get_wait_time(self, last_action):
        last_action_delay = 0
        return int(random.normalvariate(self.initiative, 0.1 * self.initiative)) + last_action_delay

    @property
    def alive(self):
        return self.hit_points > 0

class Karon(Enemy):
    def __init__(self):
        Enemy.__init__(self, 'Karon', './images/monsters/karonr.gif', 
                       attack=10, defense=10, hit_points=30, gold=21, exp=9)
