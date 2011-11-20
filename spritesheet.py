import pygame

class SpriteSheet(object):
    def __init__(self, filename, background_color=None):
        self.sheet = pygame.image.load(filename).convert()
        self.background_color = background_color
        _, _, self.width, self.height = self.sheet.get_rect()
        self._split()

    def image_at(self, rectangle, transparent=False):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size)

        image = image.convert()
        image.blit(self.sheet, (0,0), rect)

        if transparent:
            if self.background_color:
                colorkey = self.background_color
            else:
                colorkey = image.get_at((0, 0))

            image.set_colorkey(colorkey, pygame.RLEACCEL)

        return image

    def images_at(self, rects, transparent=False):
        return [self.image_at(rect, transparent) for rect in rects]

    def load_strip(self, rect, image_count, transparent=False):
        tups = [(rect[0] + rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, transparent)

    def _split(self):
        self.sprites = []
        if self.background_color is None:
            print '(0, 0) color = %s' % (str(self.sheet.get_at([0, 0])))
            return

        start_row = 0
        for y in range(self.height):
            for x in range(self.width):
                point = (x, y)
                is_background = (self.sheet.get_at(point) == self.background_color)
                if is_background:
                    #only care about real images
                    continue

                if start_row == 0:
                    #Searching for an image and found one, search for its end
                    start_row = y
                else:
                    #We're searching for the next spacer row and this is not it
                    pass
                break
            else:
                #Exhausted a spacer row
                if start_row > 0:
                    #We were searching for this, record it as a height
                    self.sprites.append(self.get_sprites(start_row, end_row=y))
                    start_row = 0


    def get_sprites(self, start_row, end_row):
        """We have a row range that sprites exist, now find the column division"""
        sprite_rects = []

        start_col = 0
        for x in range(self.width):
            for y in range(start_row, end_row):
                point = (x, y)
                is_background = (self.sheet.get_at(point) == self.background_color)
                if is_background:
                    #only care about real images
                    continue

                if start_col == 0:
                    #Searching for an image and found one, search for its end
                    start_col = x
                else:
                    #We're searching for the next spacer column and this is not it
                    pass

                break
            else:
                #Exhausted a spacer column
                if start_col > 0:
                    #We were searching for this column, record it as a width
                    sprite_rects.append([start_col, start_row,
                                         x - start_col, end_row - start_row])
                start_col = 0

        return sprite_rects

    def debug(self, desired_width, desired_height):
        ret = self.sheet.copy()
        _, _, width, height = ret.get_rect()
        debug_color = (0, 0, 0, 255)

        for row in self.rows:
            for x in xrange(width):
                ret.set_at((x, row[0]), debug_color)
                ret.set_at((x, row[0] + row[1]), debug_color)

        for column in self.columns:
            for y in xrange(height):
                ret.set_at((column[0], y), debug_color)
                ret.set_at((column[0] + column[1], y), debug_color)

        return pygame.transform.scale(ret, (desired_width, desired_height))

    def get_item(self, row, column, desired_width, desired_height, transparent=False):
        x, y, width, height = self.sprites[row][column]

        unscaled_image = self.image_at((x, y, width, height), transparent)
        return pygame.transform.scale(unscaled_image, (desired_width, desired_height))

    def sprite_width(self):
        return self.columns[0][1]

    def sprite_height(self):
        return self.rows[0][1]

