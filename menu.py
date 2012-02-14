import pygame

import items

white = (255, 255, 255)
black = (0, 0, 0)

pygame.font.init()
default_font = pygame.font.get_default_font()
#print pygame.font.get_fonts()
font_to_use = "liberationmono" #pygame.font.get_fonts()[0]
writer = pygame.font.SysFont(font_to_use, 25)
_, font_height = writer.size("A")

antialias = False
talk_option = writer.render("Talk", antialias, white, black)
spells_option = writer.render("Spells", antialias, white, black)
status_option = writer.render("Status", antialias, white, black)
items_option = writer.render("Items", antialias, white, black)
use_option = writer.render("Use", antialias, white, black)
equip_option = writer.render("Equip", antialias, white, black)

buy_option = writer.render("Buy", antialias, white, black)
sell_option = writer.render("Sell", antialias, white, black)

yes_option = writer.render("Yes", antialias, white, black)
no_option = writer.render("No", antialias, white, black)

fight_option = writer.render("Fight", antialias, white, black)
combat_spell_option = writer.render("Spell", antialias, white, black)
combat_items_option = writer.render("Item", antialias, white, black)

right_arrow_img = pygame.image.load("images/right-arrow.gif")
down_arrow_img = pygame.image.load("images/down-arrow.gif")

class BaseMenu(object):
    def __init__(self, start_time, pos, menu_items, col_width=122):
        self.arrow_img = right_arrow_img.convert()
        self.arrow_size = (40, 10)

        self.start_time = start_time

        self.pos = pos

        self.selection = [0, 0]
        self.menu_items = menu_items

        self.rows, self.cols = len(menu_items), len(menu_items[0])
        self.size = (27 + col_width * self.cols, 27 + 37 * self.rows)

    def blit_menu(self, screen, time, force_show_arrow=False):
        screen.fill(black, (self.pos + self.size))
        screen.fill(white, self.white_box)
        screen.fill(black, self.inside_box)

        blit_arrow = force_show_arrow or (time - self.start_time) % 2000 < 1000

        first_pos = (self.pos[0] + 40, self.pos[1] + 20)
        for row_idx in range(len(self.menu_items)):
            row = self.menu_items[row_idx]
            for col_idx in range(len(row)):
                item = row[col_idx]

                pos = (first_pos[0] + col_idx * 122, first_pos[1] + row_idx * 37)
                screen.blit(item, pos + (200, 10))

                if blit_arrow and [row_idx, col_idx] == self.selection:
                    arrow_pos = (pos[0] - 24, pos[1] + 3)
                    screen.blit(self.arrow_img, arrow_pos + self.arrow_size)

    def update_values(self):
        pass

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
            return {"action": "talk"}

class FightMenu(BaseMenu):
    def __init__(self, start_time):
        menu_items = [(fight_option,), (combat_spell_option,), (combat_items_option,)]
        BaseMenu.__init__(self, start_time, (40, 375), menu_items)

    def selected(self):
        selected_item = self.menu_items[self.selection[0]][0]
        if selected_item == fight_option:
            return {"action": "enemy_select", "for": "attack"}

        if selected_item == combat_spell_option:
            return {"action": "enemy_select", "for": "spell"}

        if selected_item == combat_items_option:
            return {"action": "enemy_select", "for": "item"}

        return None

class TalkMenu(object):
    @staticmethod
    def render_speach(text_lines):
        return map(lambda text: writer.render(text, antialias, white, black), text_lines)

    def __init__(self, speech_parts, num_to_close=0):
        """num_to_close, number of menus to close after finishing the talk. 0 means close_all"""
        self.arrow_img = down_arrow_img.convert()
        self.raw_speech_parts = speech_parts
        self.speech_parts = map(lambda text: TalkMenu.render_speach(text), speech_parts)
        self.speech_idx = 0

        self.pos = (100, 350)
        self.size = (650, 200)

        self.num_to_close = num_to_close

    def blit_menu(self, screen, time, force_show_arrow=False):
        screen.fill(black, (self.pos + self.size))
        screen.fill(white, self.white_box)
        screen.fill(black, self.inside_box)

        try:
            for line_idx in range(len(self.speech_parts[self.speech_idx])):
                text = self.speech_parts[self.speech_idx][line_idx]
                screen.blit(text, self.speech_box(line_idx))
        except:
            print self.raw_speech_parts

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
            to_close = self.num_to_close and "close" or "close_all"
            return {"action": to_close, "num_to_close": self.num_to_close}

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


class BuySellMenu(BaseMenu):
    def __init__(self, start_time, merchant, party):
        BaseMenu.__init__(self, start_time, (500, 200), [[buy_option], [sell_option]],
                          col_width=90)
        self.merchant = merchant
        self.party = party
        self.talk_menu = TalkMenu(merchant.greeting)

    def selected(self):
        selected_item = self.menu_items[self.selection[0]][self.selection[1]]
        if selected_item == buy_option:
            rendered_items = map(items.Item.get_rendered_buy_name, self.merchant.items_for_sale)
            ret = ItemSelectMenu(self.start_time, self.party, self.merchant,
                                 rendered_items, "buy")
        elif selected_item == sell_option:
            if len(self.party.items) == 0:
                return {"action": "menu", 
                        "menu": TalkMenu([["Sorry, you don't have anything to sell."]],
                                         num_to_close=1)}

            rendered_items = map(items.Item.get_rendered_sell_name, self.party.items)
            ret = ItemSelectMenu(self.start_time, self.party, self.merchant,
                                 rendered_items, "sell")

        return {"action": "menu", "menu": ret}

    def blit_menu(self, screen, time, force_show_arrow=False):
        self.talk_menu.blit_menu(screen, time, force_show_arrow)
        BaseMenu.blit_menu(self, screen, time, force_show_arrow)

class ItemSelectMenu(BaseMenu):
    def __init__(self, start_time, party, merchant, rendered_items, buy_or_sell):
        BaseMenu.__init__(self, start_time, (100, 200), map(lambda x: [x], rendered_items),
                          col_width=205)

        self.party = party
        self.merchant = merchant
        self.info_display = None
        self.buy_or_sell = buy_or_sell

        if buy_or_sell == "buy":
            self.talk_menu = TalkMenu([["These are my wares."]])
        elif buy_or_sell == "sell":
            self.talk_menu = TalkMenu([["What would you like to sell?"]])

    def update_values(self):
        if self.buy_or_sell == "buy":
            return

        if len(self.party.items) == 0:
            return

        items_to_sell = map(items.Item.get_rendered_sell_name, self.party.items)
        ItemSelectMenu.__init__(self, self.start_time, self.party, self.merchant,
                                items_to_sell, "sell")

    def selected(self):
        selected_item = self.merchant.items_for_sale[self.selection[1]]
        return {"action": "menu", "menu": ConfirmMenu(self.start_time, self.party,
                                                      self.merchant, selected_item,
                                                      self.buy_or_sell)}

    def blit_menu(self, screen, time, force_show_arrow=False):
        self.talk_menu.blit_menu(screen, time, force_show_arrow)

        if self.buy_or_sell == 'sell' and len(self.party.items) == 0:
            pass
        else:
            BaseMenu.blit_menu(self, screen, time, force_show_arrow)

class ConfirmMenu(BaseMenu):
    def __init__(self, start_time, party, merchant, item, buy_or_sell):
        BaseMenu.__init__(self, start_time, (510, 210), [[yes_option], [no_option]],
                          col_width=80)

        self.party = party
        self.merchant = merchant
        self.item = item
        self.buy_or_sell = buy_or_sell

        if buy_or_sell == "buy":
            self.talk_menu = TalkMenu([["Are you sure you want to buy a %s" % (item.item_name,),
                                        "for %d gold?" % (item.buy_price,)]])
        elif buy_or_sell == "sell":
            self.talk_menu = TalkMenu([["Are you sure you want to sell a %s" % (item.item_name,),
                                        "for %d gold?" % (item.sell_price,)]])
    
    def selected(self):
        selected_item = self.menu_items[0][self.selection[1]]
        if selected_item == yes_option:
            if self.buy_or_sell == "buy":
                self.party.bought(self.item)
                dialogue = TalkMenu([["You have bought a %s for %d gold." % 
                                      (self.item.item_name, self.item.buy_price)]],
                                    num_to_close=2)
            elif self.buy_or_sell == "sell":
                self.party.sold(self.item)
                #if we have nothing left to sell, go back to the buy/sell prompt
                num_to_close = self.party.items and 2 or 3
                dialogue = TalkMenu([["You have sold a %s for %d gold." %
                                      (self.item.item_name, self.item.sell_price)]],
                                    num_to_close=num_to_close)

            return {"action": "menu", "menu": dialogue}
        else: #selected_item == no_option
            return {"action": "close", "num_to_close": 1}

    def blit_menu(self, screen, time, force_show_arrow=False):
        self.talk_menu.blit_menu(screen, time, force_show_arrow)
        BaseMenu.blit_menu(self, screen, time, force_show_arrow)
