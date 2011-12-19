import random
import sounds

class CombatManager(object):
    def __init__(self, average_steps_to_fight, deviation):
	self.average_steps_to_fight = average_steps_to_fight
	self.deviation = deviation

	self.steps_to_fight = self.generate_steps_to_fight()
	print 'to fight'
	print self.steps_to_fight

    def generate_steps_to_fight(self):
	return int(random.normalvariate(self.average_steps_to_fight, self.deviation))

    def step(self, tile):
	self.steps_to_fight -= 1
	if self.steps_to_fight == 0:
	    self.steps_to_fight = self.generate_steps_to_fight()
	    return True

	if 'fight' in tile:
	    return tile['fight']

	return False

    def input(self, pygame_event):
	pass

    def generate_fight(self, frame_num):
	sounds.play_random_battle_song()
	print 'making a fight'

    def draw_combat(self, frame_num):
	pass
