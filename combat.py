import random
import sounds
import tiled_screen

white = (255, 255, 255)
black = (0, 0, 0)

class CombatManager(object):
    def __init__(self, average_steps_to_fight, deviation):
	self.average_steps_to_fight = average_steps_to_fight
	self.deviation = deviation

	self.steps_to_fight = self.generate_steps_to_fight()
        self.current_fight = None

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
        return 'fight_over'

    def generate_fight(self, screen, frame_num):
	sounds.play_random_battle_song()
        self.current_fight = Fight(screen, frame_num)

    def draw_combat(self, screen, frame_num):
        self.current_fight.draw(screen, frame_num)
        

class Fight(object):
    def __init__(self, screen, frame_num):
        self._start_frame = frame_num
        self._center = (screen.width / 2, screen.height / 2)

        seconds_for_opener = 0.5
        self._frames_for_opener = seconds_for_opener * tiled_screen.FPS

    def draw(self, screen, frame_num):
        if self._start_frame + self._frames_for_opener > frame_num - 1:
            opener_perc = (1.0 * frame_num - self._start_frame) / self._frames_for_opener
            self.draw_opener(screen, opener_perc)

        return

    def draw_opener(self, screen, opener_perc):
        box_size = (screen.width * opener_perc, screen.height * opener_perc)
        box_start_point = (self._center[0] * (1 - opener_perc),
                           self._center[1] * (1 - opener_perc))

        screen.screen.fill(black, (box_start_point + box_size))
