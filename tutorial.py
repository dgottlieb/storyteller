#!/usr/bin/python
import sys
import time

import pygame

pygame.init()
pygame.mouse.set_visible(0)

size = (screen_width, screen_height) = 320, 240
black = 0, 0, 0

screen = pygame.display.set_mode(size)

FPS = 30
MPS = 2

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

    def get_item(self, row, column, desired_width, desired_height):
        x, y = self.rows[row][0], self.columns[column][0]
        width, height = self.rows[row][1], self.columns[column][1]

        print 

        unscaled_image = self.image_at((x, y, width, height))
        return pygame.transform.scale(unscaled_image, (desired_width, desired_height))

    def sprite_width(self):
        return self.columns[0][1]

    def sprite_height(self):
        return self.rows[0][1]

sprite_background = (135, 191, 255, 255)
sheet = SpriteSheet("clean_chars.png", sprite_background)
sheet.split()

hero_down = [sheet.get_item(0, 0, 40, 40), sheet.get_item(1, 1, 40, 40)]
hero_rect = hero_down[0].get_bounding_rect()

hero_rect[0] = screen_width / 2
hero_rect[1] = screen_height / 2

total_frames = 0

clock = pygame.time.Clock()
start = time.time()

game_on = True
while game_on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_on = False

        if event.type == pygame.KEYUP:
            if event.dict['key'] == 27:
                game_on = False

    screen.fill(black)
    screen.blit(hero_down[total_frames / (FPS / MPS) % len(hero_down)], hero_rect)

    pygame.display.flip()
    total_frames += 1

    clock.tick(30)

end = time.time()
print 'Quitting...'
print 'Total Time = %.2f' % (end-start)
print 'Total Frames = %d' % (total_frames)
print 'Average FPS = %.2f' % (total_frames / (end-start))

pygame.quit()
