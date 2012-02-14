import random

import inform

class Party(object):
    def __init__(self, hero):
        self.members = [hero]
        self.items = []
        self.gold = 50

        self.status_box = inform.PartyStatus(self, right=True)
        self.gold_box = inform.GoldStatus(self)

    def __len__(self):
        return len(self.members)

    def __iter__(self):
        return iter(self.members)

    def __getitem__(self, idx):
        return self.members[idx]

    def add_gold(self, num_gold):
        self.gold += num_gold

    def add_exp(self, num_exp):
        for member in self.members:
            member.add_exp(num_exp)

    def bought(self, item):
        self.gold -= item.buy_price
        self.items.append(item)

        self.gold_box.update_values()

    def sold(self, item):
        self.gold += item.sell_price
        self.items.remove(item)

        self.gold_box.update_values()

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

        self.exp = 0

        self.str = 10
        self.agi = 10
        self.con = 10
        self.will = 10
        self.int = 10

        self.spells = []

    def __str__(self):
        return self.name

    def __getitem__(self, item_key):
        if item_key.lower() == 'hp':
            return self.hp
        elif item_key.lower() == 'mp':
            return self.mp

        return 'pc[%s] is not known' % (item_key,)

    def add_exp(self, num_exp):
        self.exp += num_exp

    @property
    def attack(self):
        return 14

    def melee(self, enemy):
        chance_to_hit = 0.9
        chance_to_crit = 0.1

        if random.random() > chance_to_hit:
            return {"action": "miss", "feedback": "You miss!", "damage": 0}

        if random.random() < chance_to_crit:
            damage = self.attack * 3
            enemy.attacked(damage)
            return {"action": "crit", "damage": damage,
                    "feedback": "You critically strike %s for %d!" % (enemy.name, damage)}

        damage = self.attack * self.attack / enemy.defense
        enemy.attacked(damage)
        return {"action": "hit", "damage": damage,
                "feedback": "You hit %s for %d!" % (enemy.name, damage)}
