import pygame

class SpriteSheet(object):
    def __init__(self, filename, background_color=(-1, -1, -1, -1)):
        self.sheet = pygame.image.load(filename).convert()
        self.background_color = background_color

    def image_at(self, rectangle, colorkey=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size)

        image = image.convert_alpha()
        image.blit(self.sheet, (0,0), rect)

        background_transparent = (self.background_color[0], self.background_color[1], 
                                  self.background_color[2], 0)
        for x in range(rectangle[-2]):
            for y in range(rectangle[-1]):
                point = (x, y)
                if image.get_at(point) == self.background_color:
                    image.set_at(point, background_transparent)

        return image

    def images_at(self, rects, colorkey=None):
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey=None):
        tups = [(rect[0] + rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

    def split(self):
        self.sprites = []
        _, _, width, height = self.sheet.get_rect()
        rows = []

        spacer_row = True
        for y in range(height):
            for x in range(width):
                point = (x, y)
                is_background = (self.sheet.get_at(point) == self.background_color)
                if is_background:
                    #only care about real images
                    continue

                if spacer_row:
                    #Searching for an image and found one, search for its end
                    rows.append([y, -1])
                    spacer_row = False
                else:
                    #We're searching for the next spacer row and this is not it
                    pass
                break
            else:
                #Exhausted a spacer row
                if not spacer_row:
                    #We were searching for this, record it as a height
                    rows[-1][-1] = y - rows[-1][0]
                spacer_row = True

        columns = []

        spacer_column = True
        for x in range(width):
            for y in range(height):
                point = (x, y)
                is_background = (self.sheet.get_at(point) == self.background_color)
                if is_background:
                    #only care about real images
                    continue

                if spacer_column:
                    #Searching for an image and found one, search for its end
                    columns.append([x, -1])
                    spacer_column = False
                else:
                    #We're searching for the next spacer column and this is not it
                    pass

                break
            else:
                #Exhausted a spacer column
                if not spacer_column:
                    #We were searching for this column, record it as a width
                    columns[-1][-1] = x - columns[-1][0]
                spacer_column = True

        self.rows = rows
        self.columns = columns

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

    def get_item(self, row, column, desired_width, desired_height):
        x, y = self.rows[row][0], self.columns[column][0]
        width, height = self.rows[row][1], self.columns[column][1]

        unscaled_image = self.image_at((x, y, width, height))
        return pygame.transform.scale(unscaled_image, (desired_width, desired_height))

    def sprite_width(self):
        return self.columns[0][1]

    def sprite_height(self):
        return self.rows[0][1]

