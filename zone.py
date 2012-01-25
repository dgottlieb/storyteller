import rpg_game
import sounds
import tiled_screen

from tiles import *

basic_tile_map = {'W': wall_tile,
                  'B': brick_tile,
                  'M': mountain_tile,
                  'H': hill_tile,
                  'G': grass_tile,
                  'T': throne_tile,
                  'S': stone_tile,
                  '.': None}

class Zone(object):
    def __init__(self):
        self.background = None
        self.npcs = []
        self.locations = {}

	self.combat_manager = None

    def music(self):
        sounds.play_music(self.music_file)

    def parse_map(self, map_strs):
        def parse_basic_tile(first_bit, second_bit, row, column):
            if second_bit == '.':
                return first_bit, None

            if first_bit == 'O':
                return oceans[int(second_bit)-1], None

            return self.parse_tile(first_bit + second_bit, row, column), (first_bit + second_bit)

        def parse_row(row_idx):
            ret = []
            row = map_strs[row_idx]
            for idx in range(len(row)/2):
                first = row[2*idx]
                second = row[2*idx+1]
                tile, tile_str = parse_basic_tile(first, second, row_idx, idx)

                if isinstance(tile, dict) and 'npc' in tile:
                    self.npcs.append(tile['npc'])

                ret.append(tile)
                if tile_str:
                    if tile_str not in self.locations:
                        self.locations[tile_str] = []
                    self.locations[tile_str].append([row_idx, idx])

            return ret

        ret = [parse_row(row_idx) for row_idx in range(len(map_strs))]
        return ret

    def get_position(self, search_tile):
        return self.locations[search_tile[0]][search_tile[1]]

    def take_actions(self, screen, party):
        tile = self.map[screen.hero_pos[0]][screen.hero_pos[1]]
	if self.combat_manager:
	    fight = self.combat_manager.step(tile)
	    if 'fight' in tile:
		pass

	    if fight:
		screen.game_state = tiled_screen.FIGHT
		self.combat_manager.generate_fight(screen, screen.total_time, party)
		screen.stop_walking()
		return None

        if not isinstance(tile, dict):
            return None

        if 'exit' in tile:
            new_zone = tile['exit'][0]()
            screen.set_zone(new_zone)
            sounds.stair_sound.play()
            screen.hero_pos = new_zone.get_position(tile['exit'][1])
            screen.set_hero_orientation(tile['exit'][2])
            screen.stop_walking()
            

    def get_tile(self, row_idx, col_idx):
        if row_idx < 0 or row_idx >= len(self.map):
            return self.background
        if col_idx < 0 or col_idx >= len(self.map[row_idx]):
            return self.background

        tile = self.map[row_idx][col_idx]
        if isinstance(tile, dict):
            return tile['tile']

        try:
            return basic_tile_map[tile]
        except KeyError:
            print row_idx, col_idx
            print tile
            print type(tile)
            raise KeyError()

    def is_wall(self, row_idx, col_idx):
        tile = self.map[row_idx][col_idx]
        if tile in ('W', 'M', 'T', 'S'):
            return True

        if isinstance(tile, dict):
            return tile.get('wall', False)

        return False

    def get_tile_info(self, row_idx, col_idx):
        if row_idx < 0 or row_idx >= len(self.map):
            return {}
        if col_idx < 0 or col_idx >= len(self.map[row_idx]):
            return {}

        tile = self.map[row_idx][col_idx]
        if isinstance(tile, str): #tile is a basic square
            return {}

        return tile #tile is a dictionary

    def get_npc_at(self, row_idx, col_idx):
        for npc in self.npcs:
            if npc.perc_moved < 0.05 and npc.row == row_idx and npc.col == col_idx:
                return npc

            if npc.perc_moved > 0.95 and npc.new_row == row_idx and npc.new_col == col_idx:
                return npc

        return None
