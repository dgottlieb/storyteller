import pygame

import tiled_screen

white = (255, 255, 255)
black = (0, 0, 0)

pygame.font.init()
default_font = pygame.font.get_default_font()
writer = pygame.font.Font(default_font, 25)

talk_option = writer.render('Talk', False, white, black)
spells_option = writer.render('Spells', False, white, black)
status_option = writer.render('Status', False, white, black)
items_option = writer.render('Items', False, white, black)
use_option = writer.render('Use', False, white, black)
equip_option = writer.render('Equip', False, white, black)

arrow_img = pygame.image.load('images/arrow.gif')

class BaseMenu(object):
    def __init__(self, start_frame_num, pos, menu_items):
        self.arrow_img = arrow_img.convert()
        self.arrow_size = (40, 10)

        self.start_frame_num = start_frame_num

        self.pos = pos

        self.selection = [0, 0]
        self.menu_items = menu_items

        rows, cols = len(menu_items), len(menu_items[0])
        self.size = (27 + 122 * cols, 27 + 37 * rows)

    def blit_menu(self, screen, frame_num):
        screen.fill(black, (self.pos + self.size))
        screen.fill(white, self.white_box)
        screen.fill(black, self.inside_box)

        blit_arrow = ((frame_num - self.start_frame_num) / 10) % 5 < 3

        first_pos = (self.pos[0] + 40, self.pos[1] + 20)
        size = (200, 10)
        for row_idx in range(len(self.menu_items)):
            row = self.menu_items[row_idx]
            for col_idx in range(len(row)):
                item = row[col_idx]

                pos = (first_pos[0] + col_idx * 122, first_pos[1] + row_idx * 37)
                screen.blit(item, pos + (200, 10))

                if blit_arrow and [row_idx, col_idx] == self.selection:
                    arrow_pos = (pos[0] - 24, pos[1] + 3)
                    screen.blit(self.arrow_img, arrow_pos + self.arrow_size)

    @property
    def white_box(self):
        new_pos = (self.pos[0] + 5, self.pos[1] + 5)
        new_size = (self.size[0] - 10, self.size[1] - 10)
        return new_pos + new_size

    @property
    def inside_box(self):
        white_box = self.white_box
        new_pos = (white_box[0] + 2, white_box[1] + 2)
        new_size = (white_box[2] - 4, white_box[3] - 4)
        return new_pos + new_size

    def move_selection(self, input_code):
        move_map = {273: (-1, 0), #UP
                    274: (1, 0), #DOWN
                    275: (0, 1), #RIGHT
                    276: (0, -1)} #LEFT

        move = move_map[input_code]
        self.selection[0] += move[0]
        self.selection[1] += move[1]

        self.selection[0] = (self.selection[0]) % len(self.menu_items)
        self.selection[1] = (self.selection[1]) % len(self.menu_items[0])

class WorldMenu(BaseMenu):
    def __init__(self, start_frame_num):
        menu_items = [(talk_option, spells_option), 
                      (status_option, items_option), 
                      (use_option, equip_option)]
        BaseMenu.__init__(self, start_frame_num, (40, 30), menu_items)

    def selected(self):
        selected_item = self.menu_items[self.selection[0]][self.selection[1]]
        if selected_item == talk_option:
            no_talker.speech_idx = 0
            return lambda frame_num: no_talker

class TalkMenu(object):
    def __init__(self, speech_parts):
        self.speech_parts = map(lambda text: writer.render(text, False, white, black), 
                                speech_parts)
        self.speech_idx = 0

        self.pos = (100, 350)
        self.size = (650, 200)

    def blit_menu(self, screen, frame):
        screen.fill(black, (self.pos + self.size))
        screen.fill(white, self.white_box)
        screen.fill(black, self.inside_box)

        screen.blit(self.speech_parts[self.speech_idx], self.speech_box)

    @property
    def white_box(self):
        new_pos = (self.pos[0] + 5, self.pos[1] + 5)
        new_size = (self.size[0] - 10, self.size[1] - 10)
        return new_pos + new_size

    @property
    def inside_box(self):
        white_box = self.white_box
        new_pos = (white_box[0] + 2, white_box[1] + 2)
        new_size = (white_box[2] - 4, white_box[3] - 4)
        return new_pos + new_size

    @property
    def speech_box(self):
        inside_box = self.inside_box
        speech_pos = (inside_box[0] + 10, inside_box[1] + 10)
        speech_size = (inside_box[2] - 5, inside_box[3] - 5)
        return speech_pos + speech_size

    def selected(self):
        self.speech_idx += 1
        if self.speech_idx == len(self.speech_parts):
            return 'close_all'

    def move_selection(self, key):
        #talk menus have no actions, ignore arrow keys
        pass


no_talker = TalkMenu(['There is no one here.'])
