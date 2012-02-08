import pygame

white = (255, 255, 255)
black = (0, 0, 0)

pygame.font.init()
default_font = pygame.font.get_default_font()
writer = pygame.font.Font(default_font, 25)
_, font_height = writer.size('A')

antialias = False
talk_option = writer.render('Talk', antialias, white, black)
spells_option = writer.render('Spells', antialias, white, black)
status_option = writer.render('Status', antialias, white, black)
items_option = writer.render('Items', antialias, white, black)
use_option = writer.render('Use', antialias, white, black)
equip_option = writer.render('Equip', antialias, white, black)

fight_option = writer.render('Fight', antialias, white, black)
combat_spell_option = writer.render('Spell', antialias, white, black)
combat_items_option = writer.render('Item', antialias, white, black)

right_arrow_img = pygame.image.load('images/right-arrow.gif')
down_arrow_img = pygame.image.load('images/down-arrow.gif')

class BaseMenu(object):
    def __init__(self, start_time, pos, menu_items):
        self.arrow_img = right_arrow_img.convert()
        self.arrow_size = (40, 10)

        self.start_time = start_time

        self.pos = pos

        self.selection = [0, 0]
        self.menu_items = menu_items

        rows, cols = len(menu_items), len(menu_items[0])
        self.size = (27 + 122 * cols, 27 + 37 * rows)

    def blit_menu(self, screen, time):
        screen.fill(black, (self.pos + self.size))
        screen.fill(white, self.white_box)
        screen.fill(black, self.inside_box)

        blit_arrow = (time - self.start_time) % 2000 < 1000

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

    def hide(self, screen):
        screen.fill(black, (self.pos + self.size))

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

    def move_selection(self, input_code, time):
        move_map = {273: (-1, 0), #UP
                    274: (1, 0), #DOWN
                    275: (0, 1), #RIGHT
                    276: (0, -1)} #LEFT

        move = move_map[input_code]
        self.selection[0] += move[0]
        self.selection[1] += move[1]

        self.selection[0] = (self.selection[0]) % len(self.menu_items)
        self.selection[1] = (self.selection[1]) % len(self.menu_items[0])

        self.start_time = time

class WorldMenu(BaseMenu):
    def __init__(self, start_time):
        menu_items = [(talk_option, spells_option), 
                      (status_option, items_option), 
                      (use_option, equip_option)]
        BaseMenu.__init__(self, start_time, (40, 30), menu_items)

    def selected(self):
        selected_item = self.menu_items[self.selection[0]][self.selection[1]]
        if selected_item == talk_option:
            return 'talk'

class FightMenu(BaseMenu):
    def __init__(self, start_time):
        menu_items = [(fight_option,), (combat_spell_option,), (combat_items_option,)]
        BaseMenu.__init__(self, start_time, (40, 375), menu_items)

    def selected(self):
        selected_item = self.menu_items[self.selection[0]][0]
        if selected_item == fight_option:
            return 'attack'

        if selected_item == combat_spell_option:
            return 'spell'

        if selected_item == combat_items_option:
            return 'item'

        return None

class TalkMenu(object):
    @staticmethod
    def render_speach(text_lines):
        return map(lambda text: writer.render(text, antialias, white, black), text_lines)

    def __init__(self, speech_parts):
        self.arrow_img = down_arrow_img.convert()
        self.speech_parts = map(lambda text: TalkMenu.render_speach(text), speech_parts)
        self.speech_idx = 0

        self.pos = (100, 350)
        self.size = (650, 200)

    def blit_menu(self, screen, time):
        screen.fill(black, (self.pos + self.size))
        screen.fill(white, self.white_box)
        screen.fill(black, self.inside_box)

        for line_idx in range(len(self.speech_parts[self.speech_idx])):
            text = self.speech_parts[self.speech_idx][line_idx]
            screen.blit(text, self.speech_box(line_idx))

        if self.speech_idx + 1 < len(self.speech_parts):
            self.blit_next_arrow(screen, time)

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

    def speech_box(self, line_num):
        inside_box = self.inside_box
        y_offset = line_num * (font_height + 3)
        speech_pos = (inside_box[0] + 10, inside_box[1] + 10 + y_offset)
        speech_size = (inside_box[2] - 5, font_height)
        return speech_pos + speech_size

    def selected(self):
        self.speech_idx += 1
        if self.speech_idx == len(self.speech_parts):
            return 'close_all'

        return None

    def move_selection(self, key, time):
        #talk menus have no actions, ignore arrow keys
        pass

    def blit_next_arrow(self, screen, time):
        if time % 2000 < 1000:
            return

        inside_box = self.inside_box
        arrow_pos = ((2*inside_box[0] + inside_box[2]) / 2 - self.arrow_img.get_width() / 2,
                     (inside_box[1] + inside_box[3]) - self.arrow_img.get_height() - 5)
        arrow_size = (40, 20)

        screen.blit(self.arrow_img, arrow_pos + arrow_size)
