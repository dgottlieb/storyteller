import sounds
from tiles import *

basic_tile_map = {'W': wall_tile,
                  'B': brick_tile,
                  'M': mountain_tile,
                  'H': hill_tile,
                  'G': grass_tile,
                  '.': None}

class Zone(object):
    def __init__(self):
        self.background = None
        self.specials = {}

    def music(self):
        sounds.play_music(self.music_file)

    def parse_map(self, map_strs):
        def parse_basic_tile(first, second):
            if second == '.':
                return first, None

            if first == 'O':
                return oceans[int(second)-1], None

            return self.parse_tile(first + second), (first + second)

        def parse_row(row_idx):
            ret = []
            row = map_strs[row_idx]
            for idx in range(len(row)/2):
                first = row[2*idx]
                second = row[2*idx+1]
                tile, special = parse_basic_tile(first, second)

                ret.append(tile)
                if special:
                    if special not in self.specials:
                        self.specials[special] = []
                    self.specials[special].append([row_idx, idx])

            return ret

        ret = [parse_row(row_idx) for row_idx in range(len(map_strs))]
        return ret

    def get_position(self, search_tile):
        return self.specials[search_tile[0]][search_tile[1]]

    def take_actions(self, screen):
        tile = self.map[screen.hero_pos[0]][screen.hero_pos[1]]
        if not isinstance(tile, dict):
            return None

        if 'exit' in tile:
            new_zone = tile['exit'][0]()
            screen.set_zone(new_zone)
            screen.hero_pos = new_zone.get_position(tile['exit'][1])
            screen.set_hero_orientation(tile['exit'][2])
            return
            

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
        if tile in ('W', 'M'):
            return True

        if isinstance(tile, dict):
            return tile.get('wall', False)

        return False
