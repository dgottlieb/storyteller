import copy

import pygame

white = (255, 255, 255)
black = (0, 0, 0)

pygame.font.init()
default_font = pygame.font.get_default_font()
writer = pygame.font.Font(default_font, 22)
_, font_height = writer.size('A')

antialias = False

class CombatLog():
    def __init__(self):
        self.rectangle = (200, 350, 425, 175)
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

class PartyStatus():
    def __init__(self, party):
        self.position = (100, 50)
        self.border_width = 2

        self.party = party
        self.height = 90

        self.stats = ["HP", "MP"]
        self.headers = map(lambda x: writer.render(x, antialias, white, black), self.stats)
        self.names = map(lambda x: writer.render(x.name, antialias, white, black), party)

    def blit(self, screen):
        screen.fill(white, self.position + (self.width, self.height))
        screen.fill(black, self.inside_box)
        for header_idx in range(len(self.headers)):
            header = self.headers[header_idx]
            screen.blit(header, self.header_box(header_idx))

        for member_idx in range(len(self.party)):
            member = self.party[member_idx]
            name_text = self.names[member_idx]

            screen.blit(name_text, self.name_box(member_idx))

            for stat_idx in range(len(self.stats)):
                stat = self.stats[stat_idx]
                value_text = writer.render(str(member[stat]), antialias, white, black)

                screen.blit(value_text, self.stat_box(member_idx, stat_idx))

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
        return [self.position[0] + 60 + x_offset,
                self.position[1] - (font_height / 2) + 3,
                75, font_height]

    @property
    def width(self):
        return 100 + len(self.party) * 100

    @property
    def inside_box(self):
        return [self.position[0] + self.border_width,
                self.position[1] + self.border_width,
                self.width - 2 * self.border_width,
                self.height - 2 * self.border_width]
