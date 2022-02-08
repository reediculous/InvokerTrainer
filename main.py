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
        sw = game.SPHERE_IMAGES["Q"].get_rect().width  # TODO: move to init
        sh = game.SPHERE_IMAGES["Q"].get_rect().height
        b = game.between_spheres_distance
        offset = (game.SIZE[0] - sw * 5 - b * 2) // 2
        for sphere in self.layout:
            game.DISPLAY.blit(
                game.SPHERE_IMAGES[sphere], (offset,
                    game.SIZE[1] - game.spheres_y_offset - sh)
            )
            offset += b + sw


class HPbar:
    HP = 100
    _status = "FULL"  # may be FULL, OKAY, LOW, CRITICAL
    MAX_WIDTH = 450
    border = 4
    width = MAX_WIDTH - border * 2
    height = 40

    def is_dead(self):
        return self.HP == 0

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

    def update_hp(self, new_val):
        self.HP += new_val
        if self.HP >= 100:
            self.HP = 100
        if self.HP < 0:
            self.HP = 0

    def get_color(self):
        R = int(255 - self.HP * 2.55)
        if R < 0:
            R = 0
        G = int(self.HP * 2.55)
        if G < 0:
            G = 0
        return R, G, 0

    def draw(self, game):
        y = game.hp_bar_y_offset
        x = game.SIZE[0] // 2 - self.MAX_WIDTH // 2
        pygame.draw.rect(game.DISPLAY, self.get_color(),
                         (x, y, self.calc_width(), self.height))


class Game:
    regime = "menu"

    ICONS_DIR = "static/images/spell_icons"
    SIZE = (500, 500)
    SPHERE_SIZE = (70, 70)
    SPHERE_SIZE_MIN = (25, 25)
    SPELL_SIZE = (100, 100)
    SPELL_SIZE_SECONDARY = (75, 75)

    COLORS = {
        "BG": (255, 255, 255),
        "TEXT": (0, 0, 0),
        "BORDER": (30, 30, 30),
        "COMBO": (255, 255, 255),
        "BORDER_SECONDARY": (80, 80, 80, 128),
    }

    SPELL_IMAGES_RAW = {}
    for s in spells.SpellInterface.spellnames:
        SPELL_IMAGES_RAW[s] = pygame.image.load(ICONS_DIR + f"/{s}.png")

    SPELL_IMAGES = {}
    for s in SPELL_IMAGES_RAW:
        SPELL_IMAGES[s] = pygame.transform.scale(SPELL_IMAGES_RAW[s], SPELL_SIZE)

    SPELL_IMAGES_SECONDARY = {}
    for s in SPELL_IMAGES_RAW:
        SPELL_IMAGES_SECONDARY[s] = pygame.transform.scale(SPELL_IMAGES_RAW[s], SPELL_SIZE_SECONDARY)
        SPELL_IMAGES_SECONDARY[s].set_alpha(128)

    SPHERE_IMAGES_RAW = {
        "Q": pygame.image.load(ICONS_DIR + "/spheres/Q.png"),
        "W": pygame.image.load(ICONS_DIR + "/spheres/W.png"),
        "E":  pygame.image.load(ICONS_DIR + "/spheres/E.png")
    }

    SPHERE_IMAGES = {
        "Q": pygame.transform.scale(SPHERE_IMAGES_RAW["Q"], SPHERE_SIZE),
        "W": pygame.transform.scale(SPHERE_IMAGES_RAW["W"], SPHERE_SIZE),
        "E": pygame.transform.scale(SPHERE_IMAGES_RAW["E"], SPHERE_SIZE)
    }

    SPHERE_IMAGES_MINIMUM = {
        "Q": pygame.transform.scale(SPHERE_IMAGES_RAW["Q"], SPHERE_SIZE_MIN),
        "W": pygame.transform.scale(SPHERE_IMAGES_RAW["W"], SPHERE_SIZE_MIN),
        "E": pygame.transform.scale(SPHERE_IMAGES_RAW["E"], SPHERE_SIZE_MIN)
    }

    POINTS = 0
    COMBO = 0
    max_combo = 0
    HPADD = 5
    HPSUB_COMBOLOST = 20
    HPSUB_TIME = 0.15

    FPS = 60
    DISPLAY = pygame.display.set_mode(SIZE)
    CLOCK = pygame.time.Clock()
    FONT = pygame.font.SysFont("Arial", 36)
    COMBOFONT = pygame.font.SysFont("Arial", 20)
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
    between_spells_distance = 20
    spell_y_offset = 250
    hp_bar_y_offset = 20
    spheres_y_offset = 50
    spell_border_width = 10
    record_offset = hp_bar_y_offset + 50
    spell_layout_offset_y = -25
    spell_layout_offset_x = -20
    combo_helper_between = 5

    running = True

    STATS_FILE_PATH = "static/stats/pac.txt"
    SETTINGS_FILE_PATH = "static/settings.txt"

    def __init__(self):
        self.functions_set = {
            "menu": {
                "events": self.process_events_main_menu,
                "draw": self.draw_menu,
            },
            "game": {
                "events": self.process_event,
                "draw": self.draw,
                "process": self.process,
            }
        }

    def finish_game(self):
        f = open(self.STATS_FILE_PATH, "a")
        f.write(str(self.POINTS) + "\t")
        f.write(str(self.max_combo) + "\n")
        f.close()
        self.regime = "menu"

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
                    self.hpbar.update_hp(self.HPADD)
                    self.COMBO += 1
                    if self.COMBO > self.max_combo:
                        self.max_combo = self.COMBO
                else:
                    self.COMBO = 0
                    self.hpbar.update_hp(-self.HPSUB_COMBOLOST)

    def process_events_main_menu(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.hpbar.HP = 100
                self.COMBO = 0
                self.max_combo = 0
                self.POINTS = 0
                self.regime = "game"

    def render_text(self):
        texts = {}
        texts["POINTS"] = \
            self.FONT.render(str(self.POINTS), True, self.COLORS["TEXT"])
        texts["COMBO"] = \
            self.FONT.render(str(self.COMBO), True, self.COLORS["TEXT"])
        return texts

    def draw(self):
        texts = self.render_text()
        self.DISPLAY.fill(self.COLORS["BG"])

        s = self.spellqueue.get_first_spell()
        sy = self.spell_y_offset
        sw = sh = self.SPELL_IMAGES["blast"].get_rect().width
        sx = self.SIZE[0] // 2 - sw // 2
        sfx = sx - self.spell_border_width
        sfy = sy - self.spell_border_width
        sfw = sw + 2 * self.spell_border_width
        sfh = sfw
        pygame.draw.rect(self.DISPLAY, self.COLORS["BORDER"],
                         (sfx, sfy, sfw, sfh))
        self.DISPLAY.blit(
            self.SPELL_IMAGES[s.name], (sx, sy)
        )

        '''
        combotext = self.COMBOFONT.render(str(s.combo), True, self.COLORS["COMBO"])
        self.DISPLAY.blit(
            combotext, (sx, sy)
        )
        '''

        helper_x = sx + self.spell_layout_offset_x
        helper_y = sy + self.spell_layout_offset_y
        w = self.SPHERE_IMAGES_MINIMUM["Q"].get_rect().width
        for char in str(s.combo):
            self.DISPLAY.blit(self.SPHERE_IMAGES_MINIMUM[char], (helper_x, helper_y))
            helper_x += self.combo_helper_between + w

        second_spell = self.spellqueue.get_k_spells(2)[1]

        sw_second = self.SPELL_IMAGES_SECONDARY["blast"].get_rect().width
        sy_second = sy - sh - self.between_spells_distance
        sx_second = sx + (self.SPELL_SIZE[0] - self.SPELL_SIZE_SECONDARY[0]) // 2
        sfx_second = sx_second - self.spell_border_width
        sfy_second = sy_second - self.spell_border_width
        sfw_second = sw_second + 2 * self.spell_border_width
        sfh_second = sfw_second
        pygame.draw.rect(self.DISPLAY, self.COLORS["BORDER_SECONDARY"],
                         (sfx_second, sfy_second, sfw_second, sfh_second), self.spell_border_width)
        self.DISPLAY.blit(
            self.SPELL_IMAGES_SECONDARY[second_spell.name],
            (sx_second, sy_second)
        )

        r = self.record_offset
        self.DISPLAY.blit(texts["COMBO"], (r, r))
        self.DISPLAY.blit(texts["POINTS"], (self.SIZE[0] - r, r))

        self.layout.draw(self)
        self.hpbar.draw(self)
        pygame.display.flip()

    def draw_menu(self):
        self.DISPLAY.fill(self.COLORS["BG"])
        text = self.FONT.render("Нажмите SPACE для начала", True, self.COLORS["TEXT"])
        self.DISPLAY.blit(text,
                          (self.SIZE[0] // 2 - text.get_rect().width // 2, self.SIZE[1] // 2 - 18))
        pygame.display.flip()

    def process(self):
        self.hpbar.update_hp(-self.HPSUB_TIME)
        self.hpbar.update_status()
        if self.hpbar.is_dead():
            self.finish_game()

    def main_loop(self):
        while self.running:
            events = pygame.event.get()
            for e in events:
                self.functions_set[self.regime]["events"](e)
            if self.regime != "menu":
                self.functions_set[self.regime]["process"]()
            self.functions_set[self.regime]["draw"]()
            self.CLOCK.tick(self.FPS)


game = Game()
game.main_loop()







