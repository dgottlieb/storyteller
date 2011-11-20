import pygame

class Screen(object):
    def __init__(self, rows, columns, tile_width, tile_height):
        self.rows = rows
        self.columns = columns
        self.tile_width = tile_width
        self.tile_height = tile_height

        self.width = tile_width * columns
        self.height = tile_height * rows

        self.screen = pygame.display.set_mode(self.size)

    @property
    def size(self):
        return (self.width, self.height)
