#!/usr/bin/python
import sys
import time

import spritesheet

import pygame

pygame.init()
pygame.mouse.set_visible(0)

size = (screen_width, screen_height) = 320, 240
black = 0, 0, 0

screen = pygame.display.set_mode(size)

FPS = 30
MPS = 2

sprite_background = (135, 191, 255, 255)
sheet = spritesheet.SpriteSheet("clean_chars.png", sprite_background)
sheet.split()

hero_down = [sheet.get_item(0, 0, 40, 40), sheet.get_item(1, 1, 40, 40)]
hero_rect = hero_down[0].get_bounding_rect()

hero_rect[0] = screen_width / 2
hero_rect[1] = screen_height / 2

total_frames = 0

clock = pygame.time.Clock()
start = time.time()

game_on = True
while game_on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_on = False

        if event.type == pygame.KEYUP:
            if event.dict['key'] == 27:
                game_on = False

    screen.fill(black)
    screen.blit(hero_down[total_frames / (FPS / MPS) % len(hero_down)], hero_rect)

    pygame.display.flip()
    total_frames += 1

    clock.tick(30)

end = time.time()
print 'Quitting...'
print 'Total Time = %.2f' % (end-start)
print 'Total Frames = %d' % (total_frames)
print 'Average FPS = %.2f' % (total_frames / (end-start))

pygame.quit()
