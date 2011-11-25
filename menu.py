import pygame

import tiled_screen

white = (255, 255, 255)
black = (0, 0, 0)

pygame.font.init()
default_font = pygame.font.get_default_font()
writer = pygame.font.Font(default_font, 25)

talk_option = writer.render('Talk', False, white, black)
arrow_img = pygame.image.load('images/arrow.gif')

BPS = 2 #blinks per second

class Menu(object):
    def __init__(self, start_frame):
        self.arrow_img = arrow_img.convert()
        self.start_frame = start_frame

    def blit_menu(self, screen, frame):
        screen.fill(black, (40, 30, 300, 325))
        screen.fill(white, (45, 35, 290, 315))
        screen.fill(black, (47, 37, 286, 311))

        if ((frame - self.start_frame) / (tiled_screen.FPS / BPS)) % 2 == 0:
            screen.blit(self.arrow_img, (60, 50, 40, 10))
        screen.blit(talk_option, (90, 50, 200, 10))
