import spritesheet

tiles_sheet = spritesheet.SpriteSheet("images/tiles.png", background_color=(0, 128, 128, 255))

mountain_tile = tiles_sheet.get_item(1, 5, 64, 64)
hill_tile = tiles_sheet.get_item(1, 4, 64, 64)
city_tile = tiles_sheet.get_item(1, 0, 64, 64)
grass_tile = tiles_sheet.get_item(1, 2, 64, 64)

brick_tile = tiles_sheet.get_item(0, 3, 64, 64)
wall_tile = tiles_sheet.get_item(0, 0, 64, 64)

stair_down_tile = tiles_sheet.get_item(0, 6, 64, 64)
stair_up_tile = tiles_sheet.get_item(0, 7, 64, 64)

castle_tile = tiles_sheet.get_item(1, 0, 64, 64)
ocean_1_tile = tiles_sheet.get_item(2, 2, 64, 64)
ocean_2_tile = tiles_sheet.get_item(2, 1, 64, 64)
ocean_3_tile = tiles_sheet.get_item(2, 8, 64, 64)
ocean_4_tile = tiles_sheet.get_item(2, 3, 64, 64)
ocean_5_tile = tiles_sheet.get_item(2, 0, 64, 64)
ocean_6_tile = tiles_sheet.get_item(2, 7, 64, 64)
ocean_7_tile = tiles_sheet.get_item(2, 4, 64, 64)
ocean_8_tile = tiles_sheet.get_item(2, 5, 64, 64)
ocean_9_tile = tiles_sheet.get_item(2, 6, 64, 64)
oceans = [ocean_1_tile, ocean_2_tile, ocean_3_tile, ocean_4_tile, ocean_5_tile,
          ocean_6_tile, ocean_7_tile, ocean_8_tile, ocean_9_tile]

oceans = map(lambda x: {'tile': x, 'wall': True}, oceans)
