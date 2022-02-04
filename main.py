import pygame

ICONS_DIR = "static/images/spell_icons"


class SphereLayout:
    layout = ""

    def add_sphere(self, k):
        if len(self.layout) < 3:
            self.layout += k
        else:
            self.layout = self.layout[1::] + k


