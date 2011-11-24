class NPC(object):
    def __init__(self, sprites, row, col):
        self.sprites = sprites
        self.row = row
        self.col = col

    def get_sprite(self, frame_number, frames_per_twitch):
        return self.sprites[(frame_number / frames_per_twitch) % len(self.sprites)]

    @property
    def width(self):
        return 64

    @property
    def height(self):
        return 64
