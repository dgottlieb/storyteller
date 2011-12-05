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

    next_possible_menu_input_frame = 0

    game_on = True
    while game_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False
                continue

            if 'key' not in event.dict:
                continue

            key = event.dict['key']
            if event.type == pygame.KEYDOWN and key == 27:
                #Escape
                game_on = False
                continue            

            if screen.game_state == tiled_screen.WORLD and \
                    event.type == pygame.KEYDOWN:

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
                elif key == 122:
                    #Z
                    if not screen.menu:
                        sounds.beep_sound.play()
                        screen.open_menu()
                        continue
                
            
            if event.type == pygame.KEYUP:
                if key in keys_down:
                    keys_down.remove(key)

                if key == 32:
                    screen.set_walking_speed(tiled_screen.MPS)

            if len(keys_down.intersection((273, 274, 275, 276))) == 0:
                #Any array key
                screen.stop_walking()

            if screen.game_state == tiled_screen.MENU and \
                    event.type == pygame.KEYDOWN:

                if key == 120:
                    #X
                    screen.close_all_menus()
                elif key in (273, 274, 275, 276):
                    if screen.total_frames < next_possible_menu_input_frame:
                        continue

                    screen.menu[-1].move_selection(key)
                    #next_possible_menu_input_frame = screen.total_frames + (0.25 * tiled_screen.FPS)
                elif key == 122:
                    #Z
                    action = screen.menu[-1].selected()
                    if action == 'close':
                        screen.close_menu()
                    elif action == 'close_all':
                        screen.close_all_menus()
                    else:
                        screen.open_menu(action)

        screen.draw()
        clock.tick(tiled_screen.FPS)

    end = time.time()
    print 'Quitting...'
    print 'Total Time = %.2f' % (end-start)
    print 'Total Frames = %d' % (screen.total_frames)
    print 'Average FPS = %.2f' % (screen.total_frames / (end-start))

    pygame.quit()
