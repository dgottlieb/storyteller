import pygame

black = (0, 0, 0)

class Enemy(object):
    def __init__(self, image_file):
        raw_surface = pygame.image.load(image_file)
        self.surface = pygame.transform.scale(raw_surface, (125, 125))

    def blit(self, screen):
        screen.blit(self.surface, (375, 225, 200, 200))

    def hide(self, screen):
        screen.fill(black, (375, 225, 200, 200))

class Karon(Enemy):
    def __init__(self):
        Enemy.__init__(self, './images/monsters/karonr.gif')
