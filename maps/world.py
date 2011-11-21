world = [
"O5O2O2O2O2O2O2O2O2O2O2O2O2O2O2O2O2O2O2O2O2O2O2O2O2O2O2O2O2O2O2O2O2O2O2O2O2O5",
"O6H.H.H.H.H.H.H.H.G.G.G.G.G.G.G.G.G.M.M.M.M.M.M.G.G.G.G.G.G.G.G.G.G.G.G.G.O4",
"O6H.H.H.H.H.H.H.G.G.G.G.G.G.G.G.G.G.M.G.G.G.G.G.G.G.G.G.G.G.G.G.G.G.G.G.G.O4",
"O6H.H.H.H.H.H.H.G.G.G.G.G.G.G.G.G.G.M.G.C0G.G.M.G.G.G.G.G.G.G.G.G.G.G.G.G.O4",
"O6H.H.H.H.H.H.H.G.G.G.G.G.G.G.G.G.G.M.G.G.G.G.M.G.G.G.G.G.G.G.G.G.G.G.G.G.O4",
"O6H.H.G.G.G.G.G.G.G.G.G.G.G.G.G.G.G.M.M.M.M.M.M.G.G.G.G.G.G.G.G.G.G.G.G.G.O4",
"O6H.H.G.G.G.G.G.G.G.G.G.G.G.G.G.G.G.H.H.H.H.H.H.G.G.G.G.G.G.G.G.G.G.G.G.G.O4",
"O5O8O8O8O8O8O8O8O8O8O8O8O8O8O8O8O8O8O8O8O8O8O8O8O8O8O8O8O8O8O8O8O8O8O8O8O8O5"]

import pygame

import castle
import zone

class World(zone.Zone):
    def __init__(self):
        zone.Zone.__init__(self)
        self.map = self.parse_map(world)
        self.background = zone.ocean_5_tile

    def music(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load('sounds/dw1overw.mid')
        pygame.mixer.music.play(-1)

    def parse_tile(self, tile_str):
        if tile_str == 'C0':
            return {'tile': zone.castle_tile,
                    'exit': (lambda: castle.Castle(), ('E0', 5))}
