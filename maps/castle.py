castle = [
"..W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.",
"..W.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.W.",
"..W.S.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.S.W.",
"..W.S.B.B.T.T.T.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.S.W.",
"..W.S.B.B.T.K0T.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.S.W.",
"..W.S.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.S.W.",
"..W.S.B.B.N0B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.S.W.",
"..W.S.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.S.W.",
"..W.S.B.B.M0B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.S.W.",
"..E0E0B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.S.W.",
"..E0E0B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.S.W.",
"..E0E0B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.S.W.",
"..E0E0B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.S.W.",
"..E0E0B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.S.W.",
"..W.S.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.S.W.",
"..W.S.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.S.W.",
"..W.S.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.S.W.",
"..W.S.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.S.W.",
"..W.S.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.S.W.",
"..W.S.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.S.W.",
"..W.S.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.S.W.",
"..W.S.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.S.W.",
"..W.S.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.S.W.",
"..W.S.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.S.W.",
"..W.S.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.B.S.W.",
"..W.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.S.W.",
"..W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W.W."]

import pygame

import chars
import items
import npc_mod
import tiles
import tiled_screen
import world
import zone


class Castle(zone.Zone):
    def __init__(self):
        zone.Zone.__init__(self)
        self.map = self.parse_map(castle)
        self.music_file = 'sounds/dw1castle.mid'

    def parse_tile(self, tile_str, row, column):
        if tile_str == 'E0':
            return {'tile': None,
                    'exit': (lambda: world.World(), ('C0', 0), tiled_screen.DOWN)}

        if tile_str == 'N0':
            walk_path = {(row, column): ((1, 0), 2),
                         (row + 1, column): ((0, 1), 2),
                         (row + 1, column + 1): ((-1, 0), 2),
                         (row, column + 1): ((0, -1), 0)}
            knight = npc_mod.NPC(chars.get_knight(), row, column, walk_path)
            return {'tile': tiles.brick_tile,
                    'npc': knight}

        if tile_str == 'K0':
            walk_path = {}
            king = npc_mod.NPC(chars.get_king(), row, column, walk_path)
            king.set_dialogue([["I am the King."], ["My life is awesome."]])
            return {'tile': tiles.brick_tile,
                    'npc': king}

        if tile_str == 'M0':
            walk_path = {}
            merchant = npc_mod.Merchant(chars.get_merchant(), row, column, walk_path,
                                        [items.stick])
            merchant.set_greeting([["What would you like to do?"]])
            return {'tile': tiles.brick_tile,
                    'npc': merchant}

    def special_actions(self, tile):
        pass
