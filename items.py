import pygame

white = (255, 255, 255)
black = (0, 0, 0)

pygame.font.init()
default_font = pygame.font.get_default_font()
writer = pygame.font.Font(default_font, 25)

antialias = False

class Item(object):
    def __init__(self, item_name):
        self.item_name = item_name
        self.buy_price = -1
        self.sell_price = -1

    def get_rendered_buy_name(self):
        if hasattr(self, "_rendered_buy"):
            return self._rendered_buy

        name_spaces = " " * (15 - len(self.item_name))
        price_spaces = " " * (5 - len(str(self.buy_price)))
        render_string = "%s%s%s%d" % (self.item_name, name_spaces, price_spaces, self.buy_price)
        self._rendered_buy = writer.render(render_string, antialias, white, black)
        return self._rendered_buy

    def get_rendered_sell_name(self):
        if hasattr(self, "_rendered_sell"):
            return self._rendered_sell

        name_spaces = " " * (15 - len(self.item_name))
        price_spaces = " " * (5 - len(str(self.sell_price)))
        render_string = "%s%s%s%d" % (self.item_name, name_spaces, price_spaces, self.sell_price)
        self._rendered_sell = writer.render(render_string, antialias, white, black)
        return self._rendered_sell

    def get_rendered_name(self):
        if hasattr(self, "_rendered"):
            return self._rendered

        self._rendered = writer.render(self.item_name, antialias, white, black)
        return self._rendered

class Equipment(Item):
    def __init__(self, item_name, stat_modifiers):
        Item.__init__(self, item_name)
        self.stat_modifiers = stat_modifiers

stick = Equipment("Stick", {})
stick.buy_price = 5
stick.sell_price = 1
