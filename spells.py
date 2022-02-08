import random
import queue


class Combo:
    """spell combo defined as dict with keys Q, W, E"""
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
    """ defines functions to work with spell combos

    fields:
        spell_to_combo
        spellnames

    method:
        get_random_spell
        init_spells_seq - returns initial Queue of spells
    """
    spell_to_combo = {
        "coldsnap": Combo("QQQ"),
        "icewall": Combo("QQE"),
        "forgespirit": Combo("EEQ"),
        "sunstrike": Combo("EEE"),
        "meteor": Combo("EEW"),
        "alacrity": Combo("WWE"),
        "EMP": Combo("WWW"),
        "tornado": Combo("WWQ"),
        "ghostwalk": Combo("QQW"),
        "blast": Combo("QWE"),
    }

    spellnames = list(spell_to_combo.keys())

    def exclude(self, spell_name):
        res = []
        for item in self.spellnames:
            if item != spell_name:
                res.append(item)
        return res

    def get_random_spell(self, prev=""):
        """returns random spell.

        :prev: string - name of previous generated spell
        if set, makes sure spell won't repeat
        """
        r = random.choice(self.exclude(prev))
        return Spell(self.spell_to_combo[r], r, r + ".png")

    def init_spells_seq(self, N):
        """returns initial Queue of spells

        params
        :N: number of spells in initial queue
        """
        seq = queue.Queue()
        prev = self.get_random_spell()
        seq.put(prev)
        for i in range(N):
            rs = self.get_random_spell(prev.name)
            prev = rs
            seq.put(rs)
        return seq


class SpellQueue:
    si = SpellInterface()

    def __init__(self, difficulty=0):
        self.queue = self.si.init_spells_seq(10)

    def add_spell(self):
        self.queue.put(self.si.get_random_spell(self.get_last_spell().name))

    def get_first_spell(self):
        return list(self.queue.queue)[0]

    def get_k_spells(self, k):
        return list(self.queue.queue)[:k:]

    def get_last_spell(self):
        return list(self.queue.queue)[-1]

    def remove_spell(self):
        return self.queue.get()
