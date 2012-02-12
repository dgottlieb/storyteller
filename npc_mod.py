import chars
import menu
import tiled_screen

move_vector_to_orientation = {(1, 0): chars.DOWN,
			      (-1, 0): chars.UP,
			      (0, 1): chars.RIGHT,
			      (0, -1): chars.LEFT}

class NPC(object):
    def __init__(self, sprites, row, col, path):
        self.sprites = sprites
        self.row = self.new_row = row
        self.col = self.new_col = col
        self.path = path
        self.time = 0
        self.moving = False

        self.offset_row = 0
        self.offset_col = 0
        self.perc_moved = 0.0

        self.dialogue = [['This human is strangely quiet. Almost as if God',
                          'had forgotten to tell it what to say.']]

    def get_sprite(self, time, seconds_per_twitch):
	sprite_idx = int(time / seconds_per_twitch / 1000)
	if self.moving:
	    orientation_slice = move_vector_to_orientation[self.direction]
	    orientation = self.sprites.__getslice__(orientation_slice[0], orientation_slice[1])
	    return orientation[sprite_idx % len(orientation)]
	    
        return self.sprites[sprite_idx % len(self.sprites)]

    @property
    def width(self):
        return 64

    @property
    def height(self):
        return 64

    def walk(self, time, hero_pos, new_hero_pos):
        if self.moving or len(self.path) == 0:
            return

        actions = self.path[(self.row, self.col)]
        new_row = self.row + actions[0][0]
        new_col = self.col + actions[0][1]

        if new_row == hero_pos[0] and new_col == hero_pos[1]:
            return

        if new_row == new_hero_pos[0] and new_col == new_hero_pos[1]:
            return

        #maybe some wall detection logic here too. Would require a handle on the map
        #the map should probably be part of the constructor

        if self.time + (actions[1] * 1000) <= time:
            self.moving = True
            self.direction = actions[0]
            self.start_time = time
            self.num_seconds = (1.0 / tiled_screen.MPS)

            self.new_row = new_row
            self.new_col = new_col

    def set_dialogue(self, dialogue):
        self.dialogue = dialogue

    def motion(self, time):
        if not self.moving:
            return

        time_passed = time - self.start_time
        self.perc_moved = 1.0 * time_passed / (self.num_seconds * 1000)

        self.offset_row = self.perc_moved * self.height * self.direction[0]
        self.offset_col = self.perc_moved * self.width * self.direction[1]

        if self.perc_moved >= 1.0:
            self.moving = False
            self.time = time
            self.start_time = 0
            self.num_seconds = 0

            self.offset_row = 0
            self.offset_col = 0
            self.perc_moved = 0.0

            self.row = self.row + self.direction[0]
            self.col = self.col + self.direction[1]
            self.direction = (0, 0)

    def talk(self, screen):
        talk_menu = menu.TalkMenu(self.dialogue)
        screen.open_menu(talk_menu)

class Merchant(NPC):
    def __init__(self, sprites, row, column, walk_path, items_for_sale):
        NPC.__init__(self, sprites, row, column, walk_path)
        self.items_for_sale = items_for_sale

    def set_greeting(self, greeting):
        self.greeting = greeting

    def talk(self, screen):
        merchant_menu = menu.BuySellMenu(screen.total_time, self, screen.party)
        screen.open_menu(merchant_menu)
