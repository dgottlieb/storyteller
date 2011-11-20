import pygame

black = (0, 0, 0)
FPS = 60

class Screen(object):
    def __init__(self, rows, columns, tile_width, tile_height):
        self.rows = rows + 2
        self.columns = columns + 2
        self.tile_width = tile_width
        self.tile_height = tile_height

        self.tile_map = {}

        self.grid = [[None for y in range(self.columns)] for x in range(self.rows)]
        self.map = ['WWWWWWWWWWWWWW',
                    'WBBBBBBBBBBBBW',
                    'WWWWWWWWWWWWWW']

        """
                    'WBBBBBBBBBBBBW',
                    'WBBBBBBBBBBBBW',
                    'WBBBBBBBBBBBBW',
                    'WBBBBBBBBBBBBW',
                    'WBBBBBBBBBBBBW',
                    'WBBBBBBBBBBBBW',
                    'WBBBBBBBBBBBBW',
                    'WBBBBBBBBBBBBW',
                    """

        self.hero_pos = [1, 2]

        self.width = tile_width * columns
        self.height = tile_height * rows

        self.screen = pygame.display.set_mode(self.size)
        self.total_frames = 0

        self.hero_rect = (columns/2 * tile_width, rows/2 * tile_height,
                          tile_width, tile_height)

        self.motioning = False
        self._next = None

        self.row_offset = 0
        self.col_offset = 0

    @property
    def size(self):
        return (self.width, self.height)
    
    """
    def tile(self, tile):
        for row in self.grid:
            for y in range(len(row)):
                row[y] = tile
                """

    def set_tile(self, char, surface):
        self.tile_map[char] = surface

    def update_grid(self):
        hero_row = self.hero_pos[0]
        hero_col = self.hero_pos[1]

        for row_idx in range(len(self.grid)):
            row = self.grid[row_idx]
            for col_idx in range(len(row)):
                map_row_idx = hero_row - self.rows/2 + row_idx
                map_col_idx = hero_col - self.columns/2 + col_idx

                if map_row_idx >= 0 and map_row_idx < len(self.map) and \
                        map_col_idx >= 0 and map_col_idx < len(self.map[map_row_idx]):
                    char = self.map[map_row_idx][map_col_idx]
                else:
                    char = None

                self.grid[row_idx][col_idx] = self.tile_map.get(char, None)

    def set_hero_up(self, hero_up_animations):
        self.hero_up = hero_up_animations
        self._hero_orientation = self.hero_up

    def set_hero_left(self, hero_left_animations):
        self.hero_left = hero_left_animations

    def set_hero_down(self, hero_down_animations):
        self.hero_down = hero_down_animations

    def set_hero_right(self, hero_right_animations):
        self.hero_right = hero_right_animations

    def moving(self, row_change, col_change):
        self.motioning = True
        self.stop_moving = False

        self.start_frame = self.total_frames
        self.num_frames = FPS / self.mps

        self.moving_rows = row_change
        self.moving_cols = col_change

    def walking_up(self):
        if self.motioning:
            self._next = self.walking_up
            return

        self.moving(-1, 0)
        self._hero_orientation = self.hero_up

    def walking_down(self):
        if self.motioning:
            self._next = self.walking_down
            return

        self.moving(1, 0)
        self._hero_orientation = self.hero_down

    def walking_left(self):
        if self.motioning:
            self._next = self.walking_left
            return

        self.moving(0, -1)
        self._hero_orientation = self.hero_left

    def walking_right(self):
        if self.motioning:
            self._next = self.walking_right
            return

        self.moving(0, 1)
        self._hero_orientation = self.hero_right

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
                    continue

                start_x = self.tile_width * (col_idx - 1) - self.col_offset
                start_y = self.tile_height * (row_idx - 1) - self.row_offset
                self.screen.blit(tile, (start_x, start_y, self.tile_width, self.tile_height))

    def blit_hero(self):
        frames_per_twitch = (FPS / self.hero_tps)
        hero_frame_idx = (self.total_frames / frames_per_twitch) % len(self._hero_orientation)
        self.screen.blit(self._hero_orientation[hero_frame_idx], self.hero_rect)

    def motion(self):
        if self.motioning == False:
            return

        perc_change = 1.0 * (self.total_frames - self.start_frame) / self.num_frames
        if perc_change < 1.0:
            self.row_offset = int(self.moving_rows * self.tile_height * perc_change)
            self.col_offset = int(self.moving_cols * self.tile_width * perc_change)
        else:
            #We finished moving a spot, update the position
            self.hero_pos[0] += self.moving_rows
            self.hero_pos[1] += self.moving_cols

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
                self.row_offset = 0
                self.col_offset = 0
                self.motioning = False
            else:
                #button is still held down, let's keep moving
                self.moving(self.moving_rows, self.moving_cols)

    def draw(self):
        self.screen.fill(black)
        self.blit_map()
        self.blit_hero()

        pygame.display.flip()

        self.total_frames += 1
