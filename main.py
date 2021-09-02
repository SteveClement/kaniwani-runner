import config # noqa

import numpy as np
import random

from kivy import platform
from kivy.app import App
from kivy.lang import Builder
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Line, Quad, Triangle
from kivy.graphics.context_instructions import Color
from kivy.properties import Clock, NumericProperty, ObjectProperty, StringProperty


debug = True

Builder.load_file("menu.kv")

if debug: Builder.load_file("debug.kv") # noqa


class MainWidget(RelativeLayout):
    from transforms import transform, transform_2d, transform_perspective # noqa
    from user_actions import keyboard_closed, on_keyboard_up, on_keyboard_down, on_touch_up, on_touch_down # noqa

    view = "2ds"

    menu_widget = ObjectProperty()
    debug_widget = ObjectProperty()

    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    if view == "2d":
        V_NO_LINES = 4
        V_LINES_SPACING = .25  # percentage in screen width

        H_NO_LINES = 15
        H_LINES_SPACING = .5  # percentage in screen height

        SPEED = .6
    else:
        V_NO_LINES = 4
        V_LINES_SPACING = .25  # percentage in screen width

        H_NO_LINES = 15
        H_LINES_SPACING = .2  # percentage in screen height

        SPEED = .5

    horizontal_lines = []
    vertical_lines = []

    current_offset_y = 0
    current_offset_x = 0
    current_speed_x = 0
    current_y_loop = 0

    tiles = []
    NO_TILES = 2
    tiles_coordinates = []

    SPEED_X = 3.0

    HITO_WIDTH = .1
    HITO_HEIGHT = .1
    HITO_BASE_Y = 0.04
    hito = None
    hito_coordinates = [(0, 0), (0, 0), (0, 0)]

    state_game_over = False
    state_game_started = False

    points = 0

    menu_title = StringProperty("KaniWani Runner \n 蟹鰐ランナー")
    menu_button_title = StringProperty(" START\nスタート")

    debug_title = StringProperty("Debug")
    debug_button_title = StringProperty("Hide")

    score_txt = StringProperty()
    hito_dbg = StringProperty()
    grid_dbg = StringProperty()
    current_tile_dbg = StringProperty()

    bgm_begin = None
    vol = 0

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        # print("Init w: {} h: {}", str(self.width), str(self.height))
        self.init_audio()
        self.init_vertical_lines()
        self.init_horizontal_lines()
        self.init_tiles()
        self.generate_tiles_coordinates()

        self.init_hito()

        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1.0 / 60)

    def init_audio(self):
        self.bgm_begin = SoundLoader.load("bgm/Annex Japanese Trap.mp3")
        self.bgm_begin.volume = 1

    def init_hito(self):
        with self.canvas:
            Color(0, 1, 0)
            self.hito = Triangle()

    def init_tiles(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.NO_TILES):
                self.tiles.append(Quad())

    def init_vertical_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.V_NO_LINES):
                self.vertical_lines.append(Line())

    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.H_NO_LINES):
                self.horizontal_lines.append(Line())

    def generate_tiles_coordinates(self):
        last_y = 0

        for i in range(len(self.tiles_coordinates)-1, -1, -1):
            if self.tiles_coordinates[i][1] < self.current_y_loop:
                del self.tiles_coordinates[i]

        if len(self.tiles_coordinates) > 0:
            last_coordinates = self.tiles_coordinates[-1]
            last_y = last_coordinates[1]+1

        for i in range(len(self.tiles_coordinates), self.NO_TILES):
            r = random.randint(-1, 1)
            self.tiles_coordinates.append((r, last_y))
            last_y += 1

    def reset_game(self):
        self.current_offset_y = 0
        self.current_y_loop = 0
        self.current_speed_x = 0
        self.current_offset_x = 0
        self.tiles_coordinates = []
        self.score_txt = f"Score: {self.current_y_loop}"
#        self.pre_fill_tiles_coordinates()
        self.generate_tiles_coordinates()
        self.state_game_over = False
        self.points = 0

    @staticmethod
    def is_desktop():
        if platform in ('linux', 'win', 'macosx'):
            return True
        return False

    def update_hito(self):
        center_x = self.width / 2
        base_y = self.HITO_BASE_Y * self.height
        hito_half_width = self.HITO_WIDTH * self.width / 2
        hito_height = self.HITO_HEIGHT * self.height

        self.hito_coordinates[0] = (center_x - hito_half_width, base_y)
        self.hito_coordinates[1] = (center_x, base_y + hito_height)
        self.hito_coordinates[2] = (center_x + hito_half_width, base_y)
        x1, y1 = self.transform(*self.hito_coordinates[0])
        x2, y2 = self.transform(*self.hito_coordinates[1])
        x3, y3 = self.transform(*self.hito_coordinates[2])

        self.hito.points = [x1, y1, x2, y2, x3, y3]

    def check_hito_collision(self):
        for i in range(0, len(self.tiles_coordinates)):
            ti_x, ti_y = self.tiles_coordinates[i]
            if ti_y > self.current_y_loop + 1:
                return False
            if self.check_hito_collision_with_tile(ti_x, ti_y):
                return False
        return True

    def check_hito_collision_with_tile(self, ti_x, ti_y):
        xmin, ymin = self.get_tile_coordinates(ti_x, ti_y)
        xmax, ymax = self.get_tile_coordinates(ti_x + 1, ti_y + 1)
        for i in range(0, 3):
            px, py = self.hito_coordinates[i]
            if xmin <= px <= xmax and ymin <= py <= ymax:
                return True
        return False

    def get_line_x_from_index(self, index):
        center_line_x = self.perspective_point_x
        spacing = self.V_LINES_SPACING * self.width
        offset = index - 0.5
        line_x = center_line_x + offset*spacing + self.current_offset_x
        return line_x

    def get_line_y_from_index(self, index):
        spacing_y = self.H_LINES_SPACING * self.height
        line_y = index * spacing_y - self.current_offset_y
        return line_y

    def get_tile_coordinates(self, ti_x, ti_y):
        ti_y -= self.current_y_loop
        x = self.get_line_x_from_index(ti_x)
        y = self.get_line_y_from_index(ti_y)
        return x, y

    def update_tiles(self):
        for i in range(0, self.NO_TILES):
            tile = self.tiles[i]
            tile_coordinates = self.tiles_coordinates[i]
            xmin, ymin = self.get_tile_coordinates(tile_coordinates[0], tile_coordinates[1])
            xmax, ymax = self.get_tile_coordinates(tile_coordinates[0]+1, tile_coordinates[1]+1)

            # 2    3
            #
            # 1    4
            x1, y1 = self.transform(xmin, ymin)
            x2, y2 = self.transform(xmin, ymax)
            x3, y3 = self.transform(xmax, ymax)
            x4, y4 = self.transform(xmax, ymin)

            tile.points = [x1, y1, x2, y2, x3, y3, x4, y4]

    def update_vertical_lines(self):
        start_index = -int(self.V_NO_LINES/2)+1
        for i in range(start_index, start_index+self.V_NO_LINES):
            line_x = self.get_line_x_from_index(i)
            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)
            self.vertical_lines[i].points = [x1, y1, x2, y2]

    def update_horizontal_lines(self):
        start_index = -int(self.V_NO_LINES/2)+1
        end_index = start_index + self.V_NO_LINES-1

        xmin = self.get_line_x_from_index(start_index)
        xmax = self.get_line_x_from_index(end_index)

        for i in range(0, self.H_NO_LINES):
            line_y = self.get_line_y_from_index(i)
            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)
            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def update(self, dt):
        time_factor = dt * 60
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.update_tiles()
        self.update_hito()

        if not self.state_game_over and self.state_game_started:
            print("running")
            speed_y = self.SPEED * self.height / 100
            self.current_offset_y += speed_y * time_factor
            speed_x = self.current_speed_x * self.width / 100
            self.current_offset_x += speed_x * time_factor
            spacing_y = self.H_LINES_SPACING * self.height
            while self.current_offset_y >= spacing_y:
                self.current_offset_y -= spacing_y
                self.current_y_loop += 1
                self.generate_tiles_coordinates()
                self.score_txt = f"Score: {self.current_y_loop}"
                self.points = self.current_y_loop

        if not self.state_game_over and self.points > 2:
            self.state_game_over = True
            self.menu_title = "  Game Over!\nゲームオーバー"
            self.menu_button_title = "  Restart?\n再開しますか"
            self.menu_widget.opacity = 1

        if not self.check_hito_collision():
            print("Touched a tile")

        self.hito_dbg = f"hito x:{int(self.current_offset_x)}"

    def on_menu_button_pressed(self):
        if self.state_game_over:
            # Play restart sound if wanted
            pass
        else:
            # play game start sound if wanted
            pass
        self.bgm_begin.play()
        self.reset_game()
        self.state_game_started = True
        self.menu_widget.opacity = 0

    def play_game_over_sound(self, dt):
        if self.state_game_over:
            pass
            # self.sound_gameover.play()

    def on_debug_button_pressed(self):
        print("debug pressed")
        self.debug = False
        self.debug_widget.opacity = 0
        for vol in np.arange(1, 0, -0.1):
            self.bgm_begin.volume = float(vol)
        self.bgm_begin.stop()


class RunnerApp(App):
    pass


RunnerApp().run()
