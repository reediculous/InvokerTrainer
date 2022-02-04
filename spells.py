import random
import queue


class Combo:
    def __init__(self, string):
        self.counter = {
            "Q": 0,
            "W": 0,
            "E": 0
        }
        for char in string:
            self.counter[char] += 1

    def __eq__(self, string):
        other = Combo(string)
        return other.counter == self.counter

    def __repr__(self):
        res = ""
        for key in self.counter:
            res += self.counter[key] * key
        return res


class Spell:
    def __init__(self, combo, name, icon=""):
        self.combo = combo
        self.name = name
        self.icon = icon


class SpellInterface:
    spell_to_combo = {
        "coldsnap": Combo("QQQ"),
        "icewall": Combo("QQE"),
        "forgespirit": Combo("QEE"),
        "sunstrike": Combo("EEE"),
        "meteor": Combo("EEW"),
        "alacrity": Combo("EWW"),
        "EMP": Combo("WWW"),
        "tornado": Combo("WWQ"),
        "ghostwalk": Combo("WQQ"),
        "blast": Combo("QWE"),
    }

    spellnames = list(spell_to_combo.keys())

    def get_random_spell(self):
        r = random.choice(self.spellnames)
        return Spell(self.spell_to_combo[r], r, r + ".png")

    def init_spells_seq(self, N):
        seq = queue.Queue()
        for i in range(N):
            rs = self.get_random_spell()
            seq.put(rs)
        return seq


class SpellQueue:
    si = SpellInterface()

    def __init__(self, difficulty=0):
        self.queue = self.si.init_spells_seq(10)

    def add_spell(self):
        self.queue.put(self.si.get_random_spell())

    def remove_spell(self):
        return self.queue.get()
