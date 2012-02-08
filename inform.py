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

    def append_line(self, text):
        output = writer.render(text, antialias, white, black)
        self.lines.append(output)

    def clear(self):
        self.lines = []
