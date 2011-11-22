#!/usr/bin/python
import sys
import time

import pygame

import chars
import sounds
import tiled_screen

keys_down = set([])

if __name__ == '__main__':
    pygame.init()
    pygame.mouse.set_visible(0)

    screen = tiled_screen.Screen(rows=9, columns=13, tile_width=64, tile_height=64)

    import maps.castle
    start_zone = maps.castle.Castle()
    screen.set_zone(start_zone)

    screen.update_grid()

    clock = pygame.time.Clock()
    start = time.time()
    total_frames = 0

    game_on = True
    while game_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False
                continue

            if event.type == pygame.KEYUP:
                if event.dict['key'] == 27:
                #Escape
                    game_on = False
                    continue            

            if event.type == pygame.KEYDOWN:
                key = event.dict['key']
                keys_down.add(key)

                if key == 273:
                    #Up key
                    screen.walking_up()
                elif key == 276:
                    #Left
                    screen.walking_left()
                elif key == 274:
                    #Down
                    screen.walking_down()
                elif key == 275:
                    #Right
                    screen.walking_right()
                elif key == 32:
                    #Spacebar
                    screen.set_walking_speed(2.5*tiled_screen.MPS)

            if event.type == pygame.KEYUP:
                key = event.dict['key']
                if key in keys_down:
                    keys_down.remove(key)

                if key == 32:
                    screen.set_walking_speed(tiled_screen.MPS)

        if len(keys_down.intersection((273, 274, 275, 276))) == 0:
            #Any array key
            screen.stop_walking()

        screen.draw()
        clock.tick(tiled_screen.FPS)

    end = time.time()
    print 'Quitting...'
    print 'Total Time = %.2f' % (end-start)
    print 'Total Frames = %d' % (screen.total_frames)
    print 'Average FPS = %.2f' % (screen.total_frames / (end-start))

    pygame.quit()
