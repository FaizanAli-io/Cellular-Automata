from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from webbrowser import open
from copy import deepcopy
from os import listdir
import random
import regex

font_family = 'Comic'


class SandPiles:
    @classmethod
    def name(cls):
        return "Sand Piles"

    def __init__(self, dims, rand=0):
        self.dims = dims  # width, height
        self.matrix = [[0 for _ in range(self.dims[0])]
                       for _ in range(self.dims[1])]
        self.changes = set()

        for _ in range(rand):
            a, b, c = random.randint(
                0, self.dims[1] - 1), random.randint(0, self.dims[0] - 1), random.randint(0, 1000)
            self.matrix[a][b] = c

    color_rules = {
        0: (0, 0, 0),
        1: (0.25, 0.25, 0.25),
        2: (0.5, 0.5, 0.5),
        3: (0.75, 0.75, 0.75),
        4: (1, 1, 1),
    }

    def color(self, i, j):
        return self.color_rules[min((4, self.matrix[i][j]))]

    def update(self):
        self.changes.clear()
        for i in range(self.dims[1]):
            for j in range(self.dims[0]):
                if self.matrix[i][j] > 3:
                    self.matrix[i][j] -= 4
                    self.changes.add((i, j))
                    if i != 0:
                        self.changes.add((i - 1, j))
                        self.matrix[i - 1][j] += 1
                    if j != 0:
                        self.changes.add((i, j - 1))
                        self.matrix[i][j - 1] += 1
                    if i != self.dims[1] - 1:
                        self.changes.add((i + 1, j))
                        self.matrix[i + 1][j] += 1
                    if j != self.dims[0] - 1:
                        self.changes.add((i, j + 1))
                        self.matrix[i][j + 1] += 1


class GameOfLife:
    @classmethod
    def name(cls):
        return "Game of Life"

    def __init__(self, dims, rand=0):
        self.dims = dims  # width, height
        self.matrix = [[0 for _ in range(self.dims[0])]
                       for _ in range(self.dims[1])]
        self.neighs = ((-1, -1), (-1, 0), (-1, 1), (0, -1),
                       (0, 1), (1, -1), (1, 0), (1, 1))
        self.changes = set()

        for _ in range(rand):
            a, b, c = random.randint(
                0, self.dims[1] - 1), random.randint(0, self.dims[0] - 1), random.randint(0, 1)
            self.matrix[a][b] = c

    color_rules = {
        0: (0, 0, 0),
        1: (1, 1, 1),
    }

    def color(self, i, j):
        return self.color_rules[self.matrix[i][j]]

    def neighbourhood(self, i, j):
        count = 0
        for x, y in self.neighs:
            try:
                count += self.matrix[i + x][j + y]
            except IndexError:
                continue
        if self.matrix[i][j]:
            return count < 2 or count > 3
        else:
            return count == 3

    def update(self):
        self.changes.clear()
        copy_matrix = deepcopy(self.matrix)
        for i in range(self.dims[1]):
            for j in range(self.dims[0]):
                if self.neighbourhood(i, j):
                    copy_matrix[i][j] = 1 if not self.matrix[i][j] else 0
                    self.changes.add((i, j))
        self.matrix = copy_matrix


class BriansBrain:
    @classmethod
    def name(cls):
        return "Brian's Brain"

    def __init__(self, dims, rand=0):
        self.dims = dims  # width, height
        self.matrix = [[0 for _ in range(self.dims[0])]
                       for _ in range(self.dims[1])]
        self.neighs = ((-1, -1), (-1, 0), (-1, 1), (0, -1),
                       (0, 1), (1, -1), (1, 0), (1, 1))
        self.changes = set()

        for _ in range(rand):
            a, b, c = random.randint(
                0, self.dims[1] - 1), random.randint(0, self.dims[0] - 1), random.randint(0, 2)
            self.matrix[a][b] = c

    color_rules = {
        0: (0, 0, 0),
        1: (0, 0, 1),
        2: (1, 1, 1)
    }

    def color(self, i, j):
        return self.color_rules[self.matrix[i][j]]

    def neighbourhood(self, i, j):
        count = 0
        for x, y in self.neighs:
            try:
                count += 1 if self.matrix[i + x][j + y] == 2 else 0
            except IndexError:
                continue
        return count == 2

    def update(self):
        self.changes.clear()
        copy_matrix = deepcopy(self.matrix)
        for i in range(self.dims[1]):
            for j in range(self.dims[0]):
                if self.matrix[i][j] == 0:
                    if self.neighbourhood(i, j):
                        copy_matrix[i][j] = 2
                        self.changes.add((i, j))
                else:
                    copy_matrix[i][j] = self.matrix[i][j] - 1
                    self.changes.add((i, j))
        self.matrix = copy_matrix


class Elementary:
    @classmethod
    def name(cls):
        return "Elementary"

    def __init__(self, dims, rule, seed=0):
        self.dims = dims  # width, height
        self.matrix = [[0 for _ in range(self.dims[0])]
                       for _ in range(self.dims[1])]
        self.changes = set()

        self.rule_set = list(map(int, list(bin(rule)[2:].zfill(8))))
        if seed == 0:
            self.current = [0 for _ in range(self.dims[0])]
            if rule % 2 == 0:
                self.current[self.dims[0] // 2] = 1
        elif seed == 1:
            self.current = [random.randint(0, 1) for _ in range(self.dims[0])]

        self.row = self.dims[0] - 1

    color_rules = {
        0: (0, 0, 0),
        1: (1, 1, 1),
    }

    def color(self, i, j):
        return self.color_rules[self.matrix[i][j]]

    def generation(self):
        next_gen = deepcopy(self.current)
        for i in range(1, len(self.current) - 1):
            index = 7 - int(''.join(map(str, self.current[i - 1:i + 2])), 2)
            next_gen[i] = self.rule_set[index]
        return next_gen

    def update(self):
        self.changes.clear()
        self.current = self.generation()
        self.matrix[self.row] = self.current
        for i in range(self.dims[0]):
            self.changes.add((self.row, i))
        self.row -= 1
        if self.row < 0:
            self.row += self.dims[0]
            self.matrix = [[0 for _ in range(self.dims[0])]
                           for _ in range(self.dims[1])]


class RockPaperScissors:
    @classmethod
    def name(cls):
        return "Rock Paper Scissors"

    def __init__(self, dims, power=9, rand=0):
        self.dims = dims  # width, height
        self.matrix = [[0 for _ in range(self.dims[0])]
                       for _ in range(self.dims[1])]
        self.changes = set()
        self.power = power
        self.matrix = [[[-1, self.power]
                        for _ in range(self.dims[0])] for _ in range(self.dims[1])]
        self.neighs = ((-1, -1), (-1, 0), (-1, 1), (0, -1),
                       (0, 1), (1, -1), (1, 0), (1, 1))
        for _ in range(rand):
            a, b, c = random.randint(
                0, self.dims[1] - 1), random.randint(0, self.dims[0] - 1), random.randint(0, 2)
            self.matrix[a][b][0] = c

    color_rules = {
        -1: (0, 0, 0),
        0: (1, 0, 0),
        1: (0, 1, 0),
        2: (0, 0, 1),
    }

    def color(self, i, j):
        return self.color_rules[self.matrix[i][j][0]]

    @staticmethod
    def beats(a, b):
        return a == (b + 1) % 3

    def update(self):
        self.changes.clear()
        fake = deepcopy(self.matrix)
        for i in range(1, self.dims[1]):
            for j in range(1, self.dims[0]):
                cell = self.matrix[i][j]
                if cell[0] == -1:
                    continue
                for x, y in self.neighs:
                    try:
                        nei = self.matrix[i + x][j + y]
                    except IndexError:
                        continue
                    if nei[0] == -1:
                        if cell[1] > 0:
                            fake[i + x][j + y] = [cell[0], cell[1] - 1]
                            self.changes.add((i+x, j+y))
                    elif self.beats(cell[0], nei[0]):
                        if nei[1] > 0:
                            fake[i + x][j + y][1] -= 1
                        else:
                            fake[i + x][j + y] = [cell[0], self.power]
                            self.changes.add((i+x, j+y))
        self.matrix = fake


class LangtonsAnt:
    @classmethod
    def name(cls):
        return "Langton's Ant"

    rule_sets = {0: "LR",
                 1: "LLRR",
                 2: "LRRL",
                 3: "RRLLLRLLLRRR",
                 4: "LRRRRRLLR", }

    def __init__(self, dims, config=0, steps=1):
        self.dims = dims  # width, height
        self.matrix = [[0 for _ in range(self.dims[0])]
                       for _ in range(self.dims[1])]
        self.changes = set()
        self.ant = [self.dims[0] // 2, self.dims[1] // 2]
        self.config = self.rule_sets[config]
        self.states = len(self.config)
        self.steps = steps
        self.dir = 0
        self.moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.safe = True

    color_rules = {
        0: (0, 0, 0),
        1: (0.1, 0.1, 0.1),
        2: (0.2, 0.2, 0.2),
        3: (0.3, 0.3, 0.3),
        4: (0.4, 0.4, 0.4),
        5: (0.5, 0.5, 0.5),
        6: (0.6, 0.6, 0.6),
        7: (0.7, 0.7, 0.7),
        8: (0.8, 0.8, 0.8),
        9: (0.9, 0.9, 0.9),
        10: (1, 1, 1),
    }

    def color(self, i, j):
        return self.color_rules[self.matrix[i][j]]

    def update(self):
        self.changes.clear()
        for i in range(self.steps):
            self.safe = (-1 < self.ant[0] < self.dims[0]
                         ) and (-1 < self.ant[1] < self.dims[1])
            if not self.safe:
                break

            self.changes.add((self.ant[0], self.ant[1]))
            val = self.matrix[self.ant[0]][self.ant[1]]
            if self.config[val] == "R":
                self.dir = (self.dir + 1) if self.dir < 3 else 0
            elif self.config[val] == "L":
                self.dir = (self.dir - 1) if self.dir > 0 else 3

            self.matrix[self.ant[0]][self.ant[1]] = (val + 1) % self.states
            x, y = self.moves[self.dir]
            self.ant[0] += x
            self.ant[1] += y


class Turmites:
    @classmethod
    def name(cls):
        return "Turmites"

    rule_sets = {0: [[[1, 2, 0], [1, 2, 1]], [[0, 1, 0], [0, 1, 1]]],
                 1: [[[1, 1, 1], [1, 8, 0]], [[1, 2, 1], [0, 1, 0]]],
                 2: [[[1, 2, 1], [0, 2, 1]], [[1, 1, 0], [1, 1, 1]]],
                 3: [[[1, 2, 1], [1, 8, 1]], [[1, 2, 1], [0, 2, 0]]],
                 4: [[[1, 8, 0], [1, 2, 1]], [[0, 2, 0], [0, 8, 1]]],
                 5: [[[1, 8, 1], [1, 8, 1]], [[1, 2, 1], [0, 1, 0]]],
                 6: [[[0, 1, 1], [0, 2, 1]], [[1, 8, 0], [0, 1, 1]]],
                 7: [[[1, 8, 1], [1, 2, 0]], [[1, 4, 1], [1, 4, 2]], [[], [0, 4, 0]]], }

    def __init__(self, dims, rule=0, steps=1):
        self.dims = dims  # width, height
        self.matrix = [[0 for _ in range(self.dims[0])]
                       for _ in range(self.dims[1])]
        self.changes = set()
        self.moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.turmite = [self.dims[0] // 2, self.dims[1] // 2]
        self.rule_set = self.rule_sets[rule]
        self.steps = steps
        self.dir = 0
        self.state = 0
        self.safe = True

    color_rules = {
        0: (0, 0, 0),
        1: (0.1, 0.1, 0.1),
        2: (0.2, 0.2, 0.2),
        3: (0.3, 0.3, 0.3),
        4: (0.4, 0.4, 0.4),
        5: (0.5, 0.5, 0.5),
        6: (0.6, 0.6, 0.6),
        7: (0.7, 0.7, 0.7),
        8: (0.8, 0.8, 0.8),
        9: (0.9, 0.9, 0.9),
        10: (1, 1, 1),
    }

    def color(self, i, j):
        return self.color_rules[self.matrix[i][j]]

    def turn(self, direct):
        if direct == 2:
            self.dir = (self.dir + 1) if self.dir < 3 else 0
        elif direct == 4:
            self.dir = (self.dir + 2) % 4
        elif direct == 8:
            self.dir = (self.dir - 1) if self.dir > 0 else 3

    def move(self):
        x, y = self.moves[self.dir]
        self.turmite[0] += x
        self.turmite[1] += y

    def update(self):
        self.changes.clear()
        for i in range(self.steps):
            self.safe = (-1 < self.turmite[0] < self.dims[0]
                         ) and (-1 < self.turmite[1] < self.dims[1])
            if not self.safe:
                break

            self.changes.add((self.turmite[0], self.turmite[1]))
            nc, dr, ns = self.rule_set[self.state][self.matrix[self.turmite[0]]
                                                   [self.turmite[1]]]
            self.matrix[self.turmite[0]][self.turmite[1]] = nc
            self.turn(dr)
            self.state = ns
            self.move()


class NumericInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        pat = regex.compile('[^0-9]')
        substring = regex.sub(pat, '', substring)
        return super(NumericInput, self).insert_text(substring, from_undo=from_undo)


class Painter(FloatLayout):
    play = False
    system = None
    draw_x, draw_y = Window.size[0] * 0.02, Window.size[1] * 0.02
    draw_w, draw_h = Window.size[0] * 0.96, Window.size[1] * 0.64
    block_x, block_y = 0.0, 0.0
    count, dimensions, block_size = 0, 0, 0.0

    def initialize(self):
        self.dimensions = self.system.dims[0]
        self.block_x, self.block_y = self.draw_w / \
            self.dimensions, self.draw_h / self.dimensions
        self.refresh()

    def reset(self):
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1)
            Line(rectangle=(self.draw_x, self.draw_y,
                 self.draw_w, self.draw_h), width=1.2)

    def refresh(self):
        self.count = 20
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1)
            Line(rectangle=(self.draw_x, self.draw_y,
                 self.draw_w, self.draw_h), width=1.2)
            for i in range(self.dimensions):
                for j in range(self.dimensions):
                    r, g, b = self.system.color(i, j)
                    Color(r, g, b)
                    Rectangle(pos=(self.draw_x + (j * self.block_x), self.draw_y + (i * self.block_y)),
                              size=(self.block_x, self.block_y))

    def update(self, _):
        if not self.play:
            return

        self.system.update()
        with self.canvas:
            for i, j in self.system.changes:
                r, g, b = self.system.color(i, j)
                Color(r, g, b)
                Rectangle(pos=(self.draw_x + (j * self.block_x), self.draw_y + (i * self.block_y)),
                          size=(self.block_x, self.block_y))

        self.count -= 1
        if self.count == 0:
            self.refresh()


class OptionsMenu(FloatLayout):
    def __init__(self, **kwargs):
        super(OptionsMenu, self).__init__(**kwargs)
        self.add_widget(Label(text="Frames\nPer Second:", pos_hint={"x": 0.06, "y": 0.8}, size_hint=(0.3, 0.1),
                              halign="left", valign="bottom", font_size=18))
        self.add_widget(Label(text="Dimensions: ", pos_hint={"x": 0.06, "y": 0.6}, size_hint=(0.3, 0.1),
                              halign="left", valign="bottom", font_size=22))
        self.frame_input = NumericInput(text="5", pos_hint={"x": 0.59, "y": 0.8}, size_hint=(0.4, 0.09),
                                        font_size=20)
        self.dims_input = NumericInput(text="80", pos_hint={"x": 0.59, "y": 0.6}, size_hint=(0.4, 0.09),
                                       font_size=20)

        self.refer_button = Button(text="Reading Material on Cellular Automata",
                                   pos_hint={"x": 0.02, "y": 0.2}, size_hint=(0.96, 0.12), font_size=13)
        self.refer_button.bind(on_release=self.linker)

        self.add_widget(self.frame_input)
        self.add_widget(self.dims_input)
        self.add_widget(self.refer_button)

    @staticmethod
    def linker(_):
        open(r"https://en.wikipedia.org/wiki/Cellular_automaton")


class Interface(FloatLayout):
    def __init__(self, **kwargs):
        super(Interface, self).__init__(**kwargs)

        self.run_button = Button(text="Generate", pos_hint={"x": 0.62, "y": 0.9}, size_hint=(0.36, 0.09), font_size=36,
                                 disabled=True, font_name=font_family)
        self.replay_button = Button(text="X", pos_hint={"x": 0.02, "y": 0.02}, size_hint=(0.15, 0.1), font_size=60,
                                    disabled=True, font_name=font_family)
        self.options_button = Button(text="O", pos_hint={"x": 0.83, "y": 0.02}, size_hint=(0.15, 0.1), font_size=60,
                                     font_name=font_family)

        self.dropdown = DropDown()
        for algo in [SandPiles, GameOfLife, BriansBrain, Elementary, RockPaperScissors, LangtonsAnt, Turmites]:
            btn = Button(text=algo.name(), size_hint_y=None,
                         height=60, font_size=32, font_name=font_family)
            btn.bind(on_release=lambda ob: self.dropdown.select(ob.text))
            self.dropdown.add_widget(btn)
        self.main_button = Button(text='Select Algorithm', pos_hint={"x": 0.02, "y": 0.9}, size_hint=(0.58, 0.09),
                                  font_size=36, font_name=font_family)
        self.main_button.bind(on_release=self.dropdown.open)

        # self.last_song = Button(text="|<<", pos_hint={"x": 0.02, "y": 0.68}, size_hint=(0.25, 0.06), disabled=True,
        #                         font_size=24, font_name=font_family)
        # self.last_song.bind(on_press=self.change_song)
        # self.next_song = Button(text=">>|", pos_hint={"x": 0.73, "y": 0.68}, size_hint=(0.25, 0.06), disabled=True,
        #                         font_size=24, font_name=font_family)
        # self.next_song.bind(on_press=self.change_song)
        # self.play_pause = Button(text="Music: Off", pos_hint={"x": 0.29, "y": 0.68}, size_hint=(0.42, 0.06),
        #                          font_size=18, font_name=font_family)
        # self.play_pause.bind(on_press=self.play_music)

        self.add_widget(self.run_button)
        self.add_widget(self.replay_button)
        self.add_widget(self.options_button)
        self.add_widget(self.main_button)

        # self.library = [
        #     (SoundLoader.load(f"./music/{file}"), file[:-4]) for file in listdir("./music")]
        # self.song_index = 0
        # random.shuffle(self.library)
        # self.sound = self.library[0][0]
        # self.song_count = len(self.library) - 1

        # self.add_widget(self.last_song)
        # self.add_widget(self.play_pause)
        # self.add_widget(self.next_song)

        self.interface_count = len(self.children)

    # def play_music(self, _):
    #     if not self.sound:
    #         print("Error: song not found")
    #         return

    #     if self.play_pause.text == "Music: Off":
    #         self.last_song.disabled = False
    #         self.next_song.disabled = False

    #     if self.sound.state == "stop":
    #         self.sound.play()

    #     elif self.sound.state == "play":
    #         self.sound.stop()

    #     self.play_pause.text = self.library[self.song_index][1]

    # def change_song(self, instance):
    #     if instance.text == "|<<":
    #         self.song_index = self.song_index - 1 if self.song_index > 0 else self.song_count
    #     elif instance.text == ">>|":
    #         self.song_index = self.song_index + 1 if self.song_index < self.song_count else 0

    #     self.sound.stop()
    #     self.sound = self.library[self.song_index][0]
    #     self.sound.play()
    #     self.play_pause.text = self.library[self.song_index][1]


class MyLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)
        self.painter = Painter()
        self.interface = Interface()
        self.options_menu = Popup(title="Options Menu",
                                  content=OptionsMenu(),
                                  size_hint=(.75, .75))

        self.painter.reset()
        self.interface.run_button.bind(on_press=self.toggle_automaton)
        self.interface.replay_button.bind(on_press=self.restart)
        self.interface.options_button.bind(on_press=self.options_menu.open)
        self.interface.dropdown.bind(on_select=self.toggle_options)
        self.event_loop = Clock.schedule_interval(
            self.painter.update, self.get_update_rate())

        self.add_widget(self.painter)
        self.add_widget(self.interface)

    def get_update_rate(self):
        return 1 / int(self.options_menu.content.frame_input.text)

    def restart(self, _):
        self.painter.play = False
        self.painter.system = self.interface.main_button.text
        self.painter.reset()
        self.interface.run_button.text = "Generate"
        self.interface.replay_button.disabled = True
        self.interface.main_button.disabled = False

    def toggle_automaton(self, instance):
        self.event_loop.cancel()
        self.event_loop = Clock.schedule_interval(
            self.painter.update, self.get_update_rate())

        if instance.text == "Generate":
            self.interface.replay_button.disabled = False
            x = int(self.options_menu.content.dims_input.text)
            dims = (x, x)

            if self.painter.system in ("Game of Life", "Brian's Brain", "Sand Piles"):
                randoms = int(self.interface.input1.text)
                if self.painter.system == "Sand Piles":
                    self.painter.system = SandPiles(dims, randoms)
                elif self.painter.system == "Game of Life":
                    self.painter.system = GameOfLife(dims, randoms)
                else:
                    self.painter.system = BriansBrain(dims, randoms)

            elif self.painter.system == "Rock Paper Scissors":
                health = int(self.interface.input1.text)
                randoms = int(self.interface.input2.text)
                self.painter.system = RockPaperScissors(dims, health, randoms)

            elif self.painter.system == "Elementary":
                rule = int(self.interface.input1.text)
                seed = int(self.interface.input2.text)
                self.painter.system = Elementary(dims, rule, seed)

            elif self.painter.system in ("Langton's Ant", "Turmites"):
                rule = int(self.interface.input1.text)
                step = int(self.interface.input2.text)
                if self.painter.system == "Langton's Ant":
                    self.painter.system = LangtonsAnt(dims, rule, step)
                else:
                    self.painter.system = Turmites(dims, rule, step)

            self.painter.initialize()
            instance.text = "Play"

        else:
            if not self.painter.play:
                self.painter.play = True
                self.interface.main_button.disabled = True
                instance.text = "Pause"
            else:
                self.painter.play = False
                self.interface.main_button.disabled = False
                instance.text = "Resume"

    def toggle_options(self, _, selection):
        self.interface.main_button.text = selection
        if self.interface.run_button.disabled:
            self.interface.run_button.disabled = False
        else:
            self.restart(None)

        unwanted = self.interface.children[:-self.interface.interface_count]
        for child in unwanted:
            self.interface.remove_widget(child)

        size = 45
        if selection in ("Game of Life", "Brian's Brain", "Sand Piles"):
            self.interface.add_widget(Label(text="Random:", pos_hint={"x": 0.06, "y": 0.8}, size_hint=(0.2, 0.06),
                                            font_size=size, font_name=font_family, halign="justify", valign="bottom"))
            self.interface.input1 = NumericInput(pos_hint={"x": 0.44, "y": 0.8}, size_hint=(0.3, 0.055), text='10',
                                                 font_size=size, font_name=font_family)
            self.interface.add_widget(self.interface.input1)

        elif selection == "Rock Paper Scissors":
            self.interface.add_widget(Label(text="Health:", pos_hint={"x": 0.04, "y": 0.8}, size_hint=(0.2, 0.06),
                                            font_size=size, font_name=font_family, halign="justify", valign="bottom"))
            self.interface.add_widget(Label(text="Random:", pos_hint={"x": 0.51, "y": 0.8}, size_hint=(0.2, 0.06),
                                            font_size=size, font_name=font_family, halign="justify", valign="bottom"))
            self.interface.input1 = NumericInput(pos_hint={"x": 0.25, "y": 0.8}, size_hint=(0.22, 0.055), text='10',
                                                 font_size=size, font_name=font_family)
            self.interface.input2 = NumericInput(pos_hint={"x": 0.75, "y": 0.8}, size_hint=(0.22, 0.055), text='20',
                                                 font_size=size, font_name=font_family)
            self.interface.add_widget(self.interface.input1)
            self.interface.add_widget(self.interface.input2)

        elif selection == "Elementary":
            self.interface.add_widget(Label(text="Rule Set:", pos_hint={"x": 0.04, "y": 0.8}, size_hint=(0.2, 0.06),
                                            font_size=size, font_name=font_family, halign="justify", valign="bottom"))
            self.interface.add_widget(Label(text="Seed:", pos_hint={"x": 0.56, "y": 0.8}, size_hint=(0.2, 0.06),
                                            font_size=size, font_name=font_family, halign="justify", valign="bottom"))
            self.interface.input1 = NumericInput(pos_hint={"x": 0.27, "y": 0.8}, size_hint=(0.22, 0.055), text='90',
                                                 font_size=size, font_name=font_family)
            self.interface.input2 = NumericInput(pos_hint={"x": 0.75, "y": 0.8}, size_hint=(0.22, 0.055), text='0',
                                                 font_size=size, font_name=font_family)
            self.interface.add_widget(self.interface.input1)
            self.interface.add_widget(self.interface.input2)

        elif selection in ("Langton's Ant", "Turmites"):
            self.interface.add_widget(Label(text="Config:", pos_hint={"x": 0.04, "y": 0.8}, size_hint=(0.2, 0.06),
                                            font_size=size, font_name=font_family, halign="justify", valign="bottom"))
            self.interface.add_widget(Label(text="Steps:", pos_hint={"x": 0.55, "y": 0.8}, size_hint=(0.2, 0.06),
                                            font_size=size, font_name=font_family, halign="justify", valign="bottom"))
            self.interface.input1 = NumericInput(pos_hint={"x": 0.25, "y": 0.8}, size_hint=(0.22, 0.055), text='0',
                                                 font_size=size, font_name=font_family)
            self.interface.input2 = NumericInput(pos_hint={"x": 0.75, "y": 0.8}, size_hint=(0.22, 0.055), text='50',
                                                 font_size=size, font_name=font_family)
            self.interface.add_widget(self.interface.input1)
            self.interface.add_widget(self.interface.input2)

        self.painter.system = selection


class MainApp(App):
    def build(self):
        return MyLayout()


if __name__ == "__main__":
    MainApp().run()
