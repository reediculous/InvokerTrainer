import pygame
import spells


pygame.init()


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
    POINTS = 0
    DISPLAY = pygame.display.set_mode(SIZE)
    CLOCK = pygame.time.Clock()
    FONT = pygame.font.SysFont("Arial", 36)
    layout = SphereLayout()
    spellqueue = spells.SpellQueue()

    KEYSET = {
        "quas": pygame.K_q,
        "wex": pygame.K_w,
        "exort": pygame.K_e,
        "invoke": pygame.K_r
    }

    running = True

    def invoke(self):
        if self.layout == self.spellqueue.get_first_spell().combo:
            self.spellqueue.remove_spell()
            return True
        return False

    def process_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == self.KEYSET["quas"]:
                self.layout.add_sphere("Q")
            if event.key == self.KEYSET["wex"]:
                self.layout.add_sphere("W")
            if event.key == self.KEYSET["exort"]:
                self.layout.add_sphere("E")
            if event.key == self.KEYSET["invoke"]:
                if self.invoke():
                    self.POINTS += 1

    def render_text(self):
        texts = {}
        texts["POINTS"] = \
            self.FONT.render(str(self.POINTS), True, self.COLORS["TEXT"])
        texts["CURRENT_SPELL"] = \
            self.FONT.render(self.spellqueue.get_first_spell().name, True, self.COLORS["TEXT"])
        return texts

    def draw(self):
        texts = self.render_text()
        self.DISPLAY.fill(self.COLORS["BG"])
        self.DISPLAY.blit(texts["CURRENT_SPELL"], (100, 100))
        pygame.display.flip()

    def main_loop(self):
        while self.running:
            events = pygame.event.get()
            for e in events:
                self.process_event(e)
            self.draw()
            self.CLOCK.tick(self.FPS)


game = Game()
game.main_loop()







