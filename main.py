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

    def draw(self, game):
        sw = game.SPHERE_IMAGES["Q"].get_rect().width
        b = game.between_spheres_distance
        offset = (game.SIZE[0] - sw * 3 - b * 2) // 2
        for sphere in self.layout:
            game.DISPLAY.blit(
                game.SPHERE_IMAGES[sphere], (offset, 300)
            )
            offset += b + sw


class HPbar:
    HP = 100
    _status = "FULL"  # may be FULL, OKAY, LOW, CRITICAL
    _COLORS = {
        "FULL": (11, 218, 81),
        "OKAY": (204, 255, 0),
        "LOW": (255, 153, 0),
        "CRITICAL": (255, 0, 43),
        "BG": (50, 50, 50)
    }
    MAX_WIDTH = 450
    border = 4
    width = MAX_WIDTH - border * 2
    height = 40

    def is_dead(self):
        return self.HP <= 0

    def update_status(self):
        if self.HP > 90:
            self._status = "FULL"
        elif self.HP > 40:
            self._status = "OKAY"
        elif self.HP > 15:
            self._status = "LOW"
        else:
            self._status = "CRITICAL"

    def calc_width(self):
        return (self.HP * self.MAX_WIDTH) // 100

    def draw(self, game):
        y = game.hp_bar_y_offset
        x = game.SIZE[0] // 2 - self.MAX_WIDTH // 2
        pygame.draw.rect(game.DISPLAY, self._COLORS[self._status],
                         (x, y, self.calc_width(), self.height))


class Game:
    ICONS_DIR = "static/images/spell_icons"
    SIZE = (500, 500)
    COLORS = {
        "BG": (255, 255, 255),
        "TEXT": (0, 0, 0)
    }
    SPELL_IMAGES = {}
    for s in spells.SpellInterface.spellnames:
        SPELL_IMAGES[s] = pygame.image.load(ICONS_DIR + f"/{s}.png")
    SPHERE_IMAGES = {
        "Q": pygame.image.load(ICONS_DIR + "/spheres/Q.png"),
        "W": pygame.image.load(ICONS_DIR + "/spheres/W.png"),
        "E":  pygame.image.load(ICONS_DIR + "/spheres/E.png")
    }
    FPS = 60
    POINTS = 0
    DISPLAY = pygame.display.set_mode(SIZE)
    CLOCK = pygame.time.Clock()
    FONT = pygame.font.SysFont("Arial", 36)
    layout = SphereLayout()
    spellqueue = spells.SpellQueue()
    hpbar = HPbar()

    KEYSET = {
        "quas": pygame.K_1,
        "wex": pygame.K_2,
        "exort": pygame.K_3,
        "invoke": pygame.K_4
    }

    between_spheres_distance = 25
    spell_y_offset = 100
    hp_bar_y_offset = 20

    running = True

    def invoke(self):
        if self.layout == self.spellqueue.get_first_spell().combo:
            self.spellqueue.remove_spell()
            self.spellqueue.add_spell()
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
                    self.hpbar.HP += 5

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
        sy = self.spell_y_offset
        sx = self.SIZE[0] // 2 - self.SPELL_IMAGES["blast"].get_rect().width // 2

        self.DISPLAY.blit(
            self.SPELL_IMAGES[self.spellqueue.get_first_spell().name], (sx, sy)
        )
        self.layout.draw(self)
        self.hpbar.draw(self)
        pygame.display.flip()

    def process(self):
        self.hpbar.HP -= 0.1
        self.hpbar.update_status()

    def main_loop(self):
        while self.running:
            events = pygame.event.get()
            for e in events:
                self.process_event(e)
            self.process()
            self.draw()
            self.CLOCK.tick(self.FPS)
            #print(self.layout)


game = Game()
game.main_loop()







