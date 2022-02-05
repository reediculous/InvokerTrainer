import pygame
import spells


class SphereLayout:
    """defines current sphere layout
    fields:
        layout - string with len of 3 containing only Q, W, E
    methods:
        add_sphere - adds new sphere to layout, deleting first one
    """
    layout = ""
    counter = {
        "Q": 0,
        "W": 0,
        "E": 0
    }

    def add_sphere(self, k):
        if k not in "QWE":
            raise ValueError
        if len(self.layout) < 3:
            self.layout += k
            self.counter[k] += 1
        else:
            self.counter[self.layout[0]] -= 1
            self.counter[k] += 1
            self.layout = self.layout[1::] + k

    def __eq__(self, combo):
        return self.counter == combo.counter


class Game:
    ICONS_DIR = "static/images/spell_icons"
    SIZE = (500, 500)
    COLORS = {
        "BG": (255, 255, 255),
        "TEXT": (0, 0, 0)
    }
    FPS = 60
    DISPLAY = pygame.display.set_mode(SIZE)
    CLOCK = pygame.time.Clock()
    layout = SphereLayout()
    spellqueue = spells.SpellQueue()

    running = True

    def invoke(self):
        #TODO: delete or not?
        if self.layout == self.spellqueue.remove_spell().combo:
            pass

    def process_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN:
            if event.KEY == pygame.K_q:
                self.layout.add_sphere("Q")
            if event.KEY == pygame.K_w:
                self.layout.add_sphere("W")
            if event.KEY == pygame.K_e:
                self.layout.add_sphere("E")





