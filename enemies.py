import pygame

black = (0, 0, 0)
white = (255, 255, 255)

enemy_width = 125
enemy_height = 125

enemy_width_buffer = 25

class Enemy(object):
    def __init__(self, image_file):
        raw_surface = pygame.image.load(image_file)
        self.surface = pygame.transform.scale(raw_surface, (enemy_width, enemy_height))

    def blit(self, screen, position, num_enemies):
        enemy_rectangle = self.enemy_rectangle(screen, position, num_enemies)
        screen.blit(self.surface, enemy_rectangle)

    def hide(self, screen, position, num_enemies):
        enemy_rectangle = self.enemy_rectangle(screen, position, num_enemies)
        screen.fill(black, enemy_rectangle)

    def enemy_rectangle(self, screen, position, num_enemies):
        fight_rectangle = self.fight_rectangle(screen)
        #screen.fill(white, fight_rectangle)

        group_rectangle_relative = self.group_rectangle(num_enemies)
        group_rectangle_absolute = ((fight_rectangle[2] - group_rectangle_relative[0]) / 2 + 
                                    fight_rectangle[0],
                                    (fight_rectangle[3] - group_rectangle_relative[1]) / 2 +
                                    fight_rectangle[1],
                                    group_rectangle_relative[0], group_rectangle_relative[1])

        #screen.fill(black, group_rectangle_absolute)

        enemy_rectangle = (group_rectangle_absolute[0] + self.enemy_offset_from_left(position),
                           group_rectangle_absolute[1],
                           enemy_width, enemy_height)

        """
        print 'call'
        print num_enemies
        print fight_rectangle
        print group_rectangle_absolute
        print enemy_rectangle
        """

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

class Karon(Enemy):
    def __init__(self):
        Enemy.__init__(self, './images/monsters/karonr.gif')
