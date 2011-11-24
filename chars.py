import spritesheet

chars_sheet = spritesheet.SpriteSheet("images/chars.png", background_color=(135, 191, 255, 255))

DOWN = [0, 2]
RIGHT = [2, 4]
LEFT = [4, 6]
UP = [6, 8]

def get_hero():
    hero = [chars_sheet.get_item(1, x, 64, 64, transparent=True) for x in range(8)]
    return hero

def get_merchant():
    merchant = [chars_sheet.get_item(7, x, 64, 64, transparent=True) for x in range(8)]
    return merchant
