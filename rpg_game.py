#!/usr/bin/python
import sys
import time

import spritesheet
import tiled_screen

import pygame

pygame.init()
pygame.mouse.set_visible(0)

black = (0, 0, 0)

FPS = 30
MPS = 2

screen = tiled_screen.Screen(rows=12, columns=12, tile_width=64, tile_height=64)

chars_sheet = spritesheet.SpriteSheet("images/chars.png", background_color=(135, 191, 255, 255))
tiles_sheet = spritesheet.SpriteSheet("images/tiles.png", background_color=(0, 128, 128, 255))

hero = [chars_sheet.get_item(1, x, 64, 64, transparent=True) for x in range(8)]
hero_rect = hero[0].get_rect()

brick_tile = tiles_sheet.get_item(0, 3, 64, 64)
brick_rect = brick_tile.get_rect()

hero_rect[0] = screen.width / 2
hero_rect[1] = screen.height / 2

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

    screen.screen.fill(black)
    screen.screen.blit(brick_tile, brick_rect)
    screen.screen.blit(hero[total_frames / (FPS / MPS) % len(hero)], hero_rect)

    pygame.display.flip()
    total_frames += 1

    clock.tick(30)

end = time.time()
print 'Quitting...'
print 'Total Time = %.2f' % (end-start)
print 'Total Frames = %d' % (total_frames)
print 'Average FPS = %.2f' % (total_frames / (end-start))

pygame.quit()
