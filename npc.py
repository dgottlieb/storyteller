import tiled_screen

class NPC(object):
    def __init__(self, sprites, row, col, path):
        self.sprites = sprites
        self.row = self.new_row = row
        self.col = self.new_col = col
        self.path = path
        self.frame = 0
        self.moving = False

        self.offset_row = 0
        self.offset_col = 0

    def get_sprite(self, frame_number, frames_per_twitch):
        return self.sprites[(frame_number / frames_per_twitch) % len(self.sprites)]

    @property
    def width(self):
        return 64

    @property
    def height(self):
        return 64

    def walk(self, frame, hero_pos, new_hero_pos):
        if self.moving or len(self.path) == 0:
            return

        actions = self.path[(self.row, self.col)]
        new_row = self.row + actions[0][0]
        new_col = self.col + actions[0][1]

        if new_row == hero_pos[0] and new_col == hero_pos[1]:
            return

        if new_row == new_hero_pos[0] and new_col == new_hero_pos[1]:
            return

        if self.frame + (tiled_screen.FPS * actions[1]) <= frame:
            self.moving = True
            self.direction = actions[0]
            self.start_frame = frame
            self.num_frames = (tiled_screen.FPS / tiled_screen.MPS)

            self.new_row = new_row
            self.new_col = new_col

    def motion(self, frame):
        if not self.moving:
            return

        frames_passed = frame - self.start_frame
        self.offset_row = 1.0 * self.height * self.direction[0] * frames_passed / self.num_frames
        self.offset_col = 1.0 * self.width * self.direction[1] * frames_passed / self.num_frames

        if frame >= self.start_frame + self.num_frames:
            self.moving = False
            self.frame = frame
            self.start_frame = 0
            self.num_frames = 0

            self.offset_row = 0
            self.offset_col = 0

            self.row = self.row + self.direction[0]
            self.col = self.col + self.direction[1]
            self.direction = (0, 0)
