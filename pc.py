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

        if random.random() > chance_to_hit:
            return {"action": "miss", "feedback": "You miss", "damage": 0}

        if random.random() < chance_to_crit:
            damage = self.attack * 3
            enemy.attacked(damage)
            return {"action": "crit", "damage": damage,
                    "feedback": "You critically strike %s for %d" % (enemy.name, damage)}

        damage = self.attack * self.attack / enemy.defense
        enemy.attacked(damage)
        return {"action": "hit", "damage": damage,
                "feedback": "You hit %s for %d" % (enemy.name, damage)}
