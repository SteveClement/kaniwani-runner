from kivy.config import Config

Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from kivy.core.window import Window

from kivy import platform

from kivy.app import App
from kivy.graphics import Line, Triangle
from kivy.graphics.context_instructions import Color
from kivy.properties import Clock, NumericProperty
from kivy.uix.widget import Widget


class MainWidget(Widget):
    from transforms import transform, transform_2d, transform_perspective
    from user_actions import keyboard_closed, on_keyboard_up, on_keyboard_down, on_touch_up, on_touch_down
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    V_NO_LINES = 4
    V_LINES_SPACING = .25  # percentage in screen width
    vertical_lines = []

    H_NO_LINES = 15
    H_LINES_SPACING = .5  # percentage in screen height
    horizontal_lines = []

    SPEED = .8
    current_offset_y = 0

    SPEED_X = 3.0
    current_offset_x = 0

    current_speed_x = 0

    HITO_WIDTH = .1
    HITO_HEIGHT = .1
    HITO_BASE_Y = 0.04
    hito = None

    state_game_over = False
    points = 1000

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        # print("Init w: {} h: {}", str(self.width), str(self.height))
        self.init_vertical_lines()
        self.init_horizontal_lines()

        self.init_hito()

        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1.0 / 60)

    @staticmethod
    def is_desktop():
        if platform in ('linux', 'win', 'macosx'):
            return True
        return False

    def init_hito(self):
        with self.canvas:
            Color(0,1,0)
            self.hito = Triangle()

    def update_hito(self):
        center_x = self.width/2
        base_y = self.HITO_BASE_Y * self.height
        hito_half_width = self.HITO_WIDTH * self.width /2
        hito_height = self.HITO_HEIGHT * self.height
        x1, y1 = self.transform(center_x - hito_half_width, base_y)
        x2, y2 = self.transform(center_x, base_y + hito_height)
        x3, y3 = self.transform(center_x + hito_half_width, base_y)

        self.hito.points = [ x1, y1, x2, y2, x3, y3 ]

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

    def update_vertical_lines(self):
        center_line_x = int(self.width / 2)
        spacing = self.V_LINES_SPACING * self.width
        offset = -int(self.V_NO_LINES / 2) + 0.5
        for i in range(0, self.V_NO_LINES):
            line_x = int(center_line_x + offset * spacing + self.current_offset_x)

            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)
            self.vertical_lines[i].points = [x1, y1, x2, y2]
            offset += 1

    def update_horizontal_lines(self):
        center_line_x = int(self.width / 2)
        spacing = self.V_LINES_SPACING * self.width
        offset = -int(self.V_NO_LINES / 2) + 0.5

        xmin = center_line_x + offset * spacing + self.current_offset_x
        xmax = center_line_x - offset * spacing + self.current_offset_x
        spacing_y = self.H_LINES_SPACING * self.height

        for i in range(0, self.H_NO_LINES):
            line_y = i * spacing_y - self.current_offset_y

            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)
            self.horizontal_lines[i].points = [x1, y1, x2, y2]


    def update(self, dt):
        time_factor = dt * 60
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.update_hito()

        if not self.state_game_over:
            speed_y = self.SPEED * self.height /100
            self.current_offset_y += speed_y * time_factor

            speed_x = self.current_speed_x * self.width / 100
            self.current_offset_x += speed_x * time_factor

            spacing_y = self.H_LINES_SPACING * self.height
            while self.current_offset_y >= spacing_y:
                self.current_offset_y -= spacing_y

        if not self.state_game_over and self.points < 100:
            self.state_game_over = True
            print("Game over!")


class GalaxyApp(App):
    pass


GalaxyApp().run()
