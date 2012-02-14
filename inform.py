import copy

import pygame

white = (255, 255, 255)
black = (0, 0, 0)

pygame.font.init()
default_font = pygame.font.get_default_font()
font_to_use = "liberationmono" #pygame.font.get_fonts()[0]
writer = pygame.font.SysFont(font_to_use, 22)
_, font_height = writer.size('A')

antialias = False

class CombatLog():
    def __init__(self):
        self.rectangle = (200, 350, 500, 175)
        self.border_width = 2

        self.lines = []

    def blit(self, screen):
        screen.fill(white, self.rectangle)
        screen.fill(black, self.inside_box)

        for line_idx in range(len(self.lines)):
            line = self.lines[line_idx]
            y_offset = line_idx * (font_height + 5)
            position = (self.rectangle[0] + 20, 
                        self.rectangle[1] + 20 + y_offset)
            screen.blit(line, position + (200, 15))

    def hide(self, screen):
        screen.fill(black, self.rectangle)
 
    @property
    def inside_box(self):
        return [self.rectangle[0] + self.border_width,
                self.rectangle[1] + self.border_width,
                self.rectangle[2] - 2 * self.border_width,
                self.rectangle[3] - 2 * self.border_width]

    def append(self, text):
        output = writer.render(text, antialias, white, black)
        self.lines.append(output)

    def clear(self):
        self.lines = []

class PartyStatus(object):
    def __init__(self, party, right=False):
        if right:
            self.position = (500, 30)
        else:
            self.position = (100, 50)

        self.border_width = 2

        self.party = party
        self.height = 90

        self.stats = ["HP", "MP"]
        self.headers = map(lambda x: writer.render(x, antialias, white, black), self.stats)
        self.names = map(lambda x: writer.render(x.name, antialias, white, black), party)

        self._cached_members = [] #to be clear what is being set below
        self.update_values()

    def update_values(self):
        self._cached_members = []
        for member in self.party:
            member_stats = []
            for stat_idx in range(len(self.stats)):
                stat = self.stats[stat_idx]
                value_text = writer.render(str(member[stat]), antialias, white, black)

                member_stats.append(value_text)

            self._cached_members.append(member_stats)
            

    def blit(self, screen):
        screen.fill(white, self.position + (self.width, self.height))
        screen.fill(black, self.inside_box)
        for header_idx in range(len(self.headers)):
            header = self.headers[header_idx]
            screen.blit(header, self.header_box(header_idx))

        for member_idx in range(len(self.party)):
            name_text = self.names[member_idx]
            cached_member_stats = self._cached_members[member_idx]

            screen.blit(name_text, self.name_box(member_idx))
            for stat_idx in range(len(self.stats)):
                stat = cached_member_stats[stat_idx]
                screen.blit(stat, self.stat_box(member_idx, stat_idx))

    def stat_box(self, column, row):
        x_offset = column * 75
        y_offset = row * (font_height + 5)

        return [self.position[0] + 60 + x_offset,
                self.position[1] + font_height + y_offset,
                75, font_height]

    def header_box(self, idx):
        y_offset = idx * (font_height + 5)
        return [self.position[0] + 10,
                self.position[1] + font_height + y_offset,
                50, font_height]

    def name_box(self, idx):
        x_offset = idx * 75
        return [self.position[0] + 55 + x_offset,
                self.position[1] - (font_height / 2) + 3,
                75, font_height]

    @property
    def width(self):
        return 50 + len(self.party) * 75

    @property
    def inside_box(self):
        return [self.position[0] + self.border_width,
                self.position[1] + self.border_width,
                self.width - 2 * self.border_width,
                self.height - 2 * self.border_width]

class GoldStatus(object):
    def __init__(self, party):
        self.border_width = 2
        self.party = party

        self.pos = (650, 200)
        self.size = (100, 55)

        self.header = writer.render("Gold", antialias, white, black)
        self.value = None #to be clear what is being set below
        self.update_values()

    def update_values(self):
        spaces = " " * (6 - len(str(self.party.gold)))
        self.value = writer.render(spaces + str(self.party.gold), antialias, white, black)

    def blit(self, screen):
        screen.fill(black, self.box)
        screen.fill(white, self.border_box)
        screen.fill(black, self.inside_box)

        screen.blit(self.header, self.header_box)
        screen.blit(self.value, self.value_box)

    @property
    def box(self):
        return self.pos + self.size

    @property
    def border_box(self):
        new_pos = (self.pos[0] + self.border_width, self.pos[1] + self.border_width)
        new_size = (self.size[0] - 2 * self.border_width, self.size[1] - 2 * self.border_width)
        return new_pos + new_size

    @property
    def inside_box(self):
        new_pos = (self.pos[0] + 2 * self.border_width, self.pos[1] + 2 * self.border_width)
        new_size = (self.size[0] - 4 * self.border_width, self.size[1] - 4 * self.border_width)
        return new_pos + new_size

    @property
    def header_box(self):
        x_offset = 40
        y_offset = -4
        return (self.pos[0] + x_offset, self.pos[1] + y_offset, 0, font_height)

    @property
    def value_box(self):
        x_offset = 10
        y_offset = font_height - 3
        return (self.pos[0] + x_offset, self.pos[1] + y_offset, 0, font_height)
