import random

class Party(object):
    def __init__(self, hero):
        self.members = [hero]
        self.items = []

class PC(object):
    def __init__(self, name):
        self.name = name

        self.helmet = None
        self.armor = None
        self.gloves = None
        self.pants = None
        self.boots = None

        self.weapon = None
        self.offhand = None

        self.max_hp = 25
        self.max_mp = 15

        self.hp = 25
        self.mp = 15

        self.str = 10
        self.agi = 10
        self.con = 10
        self.will = 10
        self.int = 10

        self.spells = []    

    def __str__(self):
        return self.name

    @property
    def attack(self):
        return 14

    def melee(self, enemy):
        chance_to_hit = 0.9
        chance_to_crit = 0.1

        enemy.attacked(16)
        return 'hit'

        if random.random() > chance_to_hit:
            return 'miss'

        if random.random() < chance_to_crit:
            enemy.attacked(self.attack * 3)
            print 'Critted for %d, %d HP remains' % (self.attack * 3, enemy.hit_points)
            return 'crit'

        dmg = self.attack * self.attack / enemy.defense
        enemy.attacked(dmg)
        print 'Hit for %d, %d HP remains' % (dmg, enemy.hit_points)
        return 'hit'
