import time

import pygame

import chars
import inform
import menu
import pc
import sounds

black = (0, 0, 0)
black_tile = pygame.Surface((64, 64))
white = (255, 255, 255)
MAX_FPS = 100

TPS = 2 #Twitches per second, characters transitioning between different states
MPS = 3 #Movement per second, how many tiles the hero can walk per second

WORLD = 0
MENU = 1
FIGHT = 2

UP = 'UP'
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'

DIRECTIONS = {UP: (-1, 0),
              DOWN: (1, 0),
              LEFT: (0, -1),
              RIGHT: (0, 1)}

ORIENTATION = {UP: chars.UP,
               DOWN: chars.DOWN,
               LEFT: chars.LEFT,
               RIGHT: chars.RIGHT}

class Screen(object):
    def __init__(self, rows, columns, tile_width, tile_height):
        self.rows = rows + 2
        self.columns = columns + 2
        self.tile_width = tile_width
        self.tile_height = tile_height

        self.tile_map = {}

        self.grid = [[None for y in range(self.columns)] for x in range(self.rows)]

        self.width = tile_width * columns
        self.height = tile_height * rows

        self.world_frames = 0
	self.total_frames = 0

	self.world_time = 0
	self.total_time = 0

        self.screen = pygame.display.set_mode(self.size)

        self.hero_animations = chars.get_hero()
        self.set_hero_tps(TPS)
        self.set_walking_speed(MPS)

        self.hero_pos = self.hero_new_pos = [9, 3] #load from savegame
        self.set_hero_orientation(DOWN)

        self.hero_rect = (columns/2 * tile_width, rows/2 * tile_height,
                          tile_width, tile_height)

        self.motioning = False
        self._next = None

        self.row_offset = 0
        self.col_offset = 0

        self.menu = []
        self.game_state = WORLD

        self.party = pc.Party(pc.PC('Dan'))

    @property
    def size(self):
        return (self.width, self.height)

    def set_zone(self, zone):
        self.zone = zone
        zone.music()

    def set_tile(self, char, surface):
        self.tile_map[char] = surface

    def set_stair_sound(self, stair_sound):
        self.stair_sound = stair_sound

    def update_grid(self):
        hero_row = self.hero_pos[0]
        hero_col = self.hero_pos[1]

        for row_idx in range(len(self.grid)):
            row = self.grid[row_idx]
            for col_idx in range(len(row)):
                map_row_idx = hero_row - self.rows/2 + row_idx
                map_col_idx = hero_col - self.columns/2 + col_idx

                tile = self.zone.get_tile(map_row_idx, map_col_idx)
                self.grid[row_idx][col_idx] = tile

    def set_hero_orientation(self, direction):
        self._hero_direction = direction

        orientation_slice = ORIENTATION[direction]
        self._hero_orientation = self.hero_animations.__getslice__(orientation_slice[0],
                                                                   orientation_slice[1])

    def moving(self, tile_change):
        row_change, col_change = tile_change
        new_row = self.hero_pos[0] + row_change
        new_col = self.hero_pos[1] + col_change
        if self.zone.is_wall(new_row, new_col):
            sounds.bump_sound.play()
            self.stop_walking()
            self.motioning = False
            return

        for npc in self.zone.npcs:
            if npc.row == new_row and npc.col == new_col:
                sounds.bump_sound.play()
                self.stop_walking()
                self.motioning = False
                return

            if npc.new_row == new_row and npc.new_col == new_col:
                sounds.bump_sound.play()
                self.stop_walking()
                self.motioning = False
                return                

        sounds.bump_sound.stop()

        self.motioning = True
        self.stop_moving = False

        self.start_time = self.world_time
	self.num_time = 1.0 / self.mps * 1000

        self.moving_rows = row_change
        self.moving_cols = col_change

        self.hero_new_pos = (new_row, new_col)

    def walking_up(self):
        if self.motioning:
            self._next = self.walking_up
            return

        self.moving(DIRECTIONS[UP])
        self.set_hero_orientation(UP)

    def walking_down(self):
        if self.motioning:
            self._next = self.walking_down
            return

        self.moving(DIRECTIONS[DOWN])
        self.set_hero_orientation(DOWN)

    def walking_left(self):
        if self.motioning:
            self._next = self.walking_left
            return

        self.moving(DIRECTIONS[LEFT])
        self.set_hero_orientation(LEFT)

    def walking_right(self):
        if self.motioning:
            self._next = self.walking_right
            return

        self.moving(DIRECTIONS[RIGHT])
        self.set_hero_orientation(RIGHT)

    def set_hero_tps(self, tps):
        self.hero_tps = tps

    def set_walking_speed(self, mps):
        self.mps = mps

    def stop_walking(self):
        self.stop_moving = True

    def blit_map(self):
        self.motion()
        for row_idx in range(len(self.grid)):
            for col_idx in range(len(self.grid[row_idx])):
                tile = self.grid[row_idx][col_idx]
                if not tile:
		    tile = self.zone.background or black_tile

                start_x = self.tile_width * (col_idx - 1) - self.col_offset
                start_y = self.tile_height * (row_idx - 1) - self.row_offset
                self.screen.blit(tile, (start_x, start_y, self.tile_width, self.tile_height))

    def blit_hero(self):
        seconds_per_twitch = (1.0 / self.hero_tps)
        hero_sprite_idx = int(self.world_time / seconds_per_twitch / 1000) % len(self._hero_orientation)
        self.screen.blit(self._hero_orientation[hero_sprite_idx], self.hero_rect)

    def blit_npcs(self):
        for npc in self.zone.npcs:
            rel_row = npc.row - self.hero_pos[0] + (self.rows/2)
            rel_col = npc.col - self.hero_pos[1] + (self.columns/2)
            if rel_row < 0 or rel_row > self.rows:
                continue

            if rel_col < 0 or rel_col > self.columns:
                continue                    

            seconds_per_twitch = (1.0 / self.hero_tps)
            npc_sprite = npc.get_sprite(self.world_time, seconds_per_twitch)

            start_x = npc.width * (rel_col - 1) + npc.offset_col - self.col_offset
            start_y = npc.height * (rel_row - 1) + npc.offset_row - self.row_offset
            self.screen.blit(npc_sprite, (start_x, start_y, npc.width, npc.height))

    def motion(self):
        for npc in self.zone.npcs:
            npc.walk(self.world_time, self.hero_pos, self.hero_new_pos)
            npc.motion(self.world_time)

        if self.motioning == False:
            return

        perc_change = 1.0 * (self.world_time - self.start_time) / self.num_time
        if perc_change < 1.0:
            self.row_offset = int(self.moving_rows * self.tile_height * perc_change)
            self.col_offset = int(self.moving_cols * self.tile_width * perc_change)
            return;

        #We finished moving a spot, update the position
        self.row_offset = 0
        self.col_offset = 0
        self.hero_pos[0] += self.moving_rows
        self.hero_pos[1] += self.moving_cols

        #take actions for the new spot
        self.zone.take_actions(self, self.party)

        #and update the slice of the map
        self.update_grid()            

        if self._next:
            #Was another move queued up? If so, execute it
            self.motioning = False
            self._next()
            self._next = None
            return

        if self.stop_moving:
            #button was let go, stop motioning
            self.motioning = False
        else:
            #button is still held down, let's keep moving
            self.moving((self.moving_rows, self.moving_cols))

    def get_facing_square(self):
        row, column = self.hero_pos 
        delta_row, delta_column = DIRECTIONS[self._hero_direction]

        return row + delta_row, column + delta_column

    def open_menu(self, new_menu=None):
        self.game_state = MENU
        if not new_menu:
            self.party.status_box.update_values()
            self.party.gold_box.update_values()

            self.menu.append(menu.WorldMenu(self.total_time)) #WorldMenu(frames)
            self.menu[-1].blit_menu(self.screen, self.total_time) #blit_menu(screen, frames)
        else:
            self.menu.append(new_menu)

    def close_menu(self):
        self.menu.pop()
        if not self.menu:
            self.game_state = WORLD
        else:
            self.party.status_box.update_values()
            self.party.gold_box.update_values()

            self.draw_world()
            for menu in self.menu:
                menu.update_values()
                menu.blit_menu(self.screen, self.total_time, force_show_arrow=True)

    def close_all_menus(self):
        while self.menu:
            self.close_menu()

    def draw_world(self):
        self.blit_map()
        self.blit_hero()
        self.blit_npcs()

    def draw(self, time_elapsed):
        if self.game_state == MENU:
            self.party.status_box.blit(self.screen)
            self.party.gold_box.blit(self.screen)

            self.menu[-1].blit_menu(self.screen, self.total_time) #blit_menu(screen, frames)
	elif self.game_state == FIGHT:
	    self.zone.combat_manager.draw_combat(self, self.total_time) #draw_combat(self, frames)
	    #self.game_state = WORLD
        elif self.game_state == WORLD:
            self.draw_world()

        pygame.display.flip()

        if self.game_state == WORLD:
            self.world_frames += 1
	    self.world_time += time_elapsed

	self.total_frames += 1
	self.total_time += time_elapsed
