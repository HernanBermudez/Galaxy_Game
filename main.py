from kivy.config import Config

Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from kivy import platform
from kivy.core.window import Window
from kivy.app import App
from kivy.graphics import Color, Line
from kivy.properties import NumericProperty, Clock
from kivy.uix.widget import Widget

class MainWidget(Widget):

    from transforms import transform, transform_2D, transform_perspective
    from user_actions import on_keyboard_down, on_keyboard_up, on_touch_down, on_touch_up, keyboard_closed
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)
    vertical_lines = []
    V_NB_LINES = 10
    V_LINES_SPACING = .25 # porcentaje del ancho de la pantalla

    horizontal_lines = []
    H_NB_LINES = 8
    H_LINES_SPACING = .1  # porcentaje del ancho de la pantalla

    current_offset_y = 0
    speed = 1
    speed_x = 12
    current_speed_x = 0
    current_offset_x = 0

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.init_vertical_lines()
        self.init_horizontal_lines()
        # print("INIT W:" +str(self.width) + "H:" + str(self.height))
        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1 / 60)

    def is_desktop(self):
        if platform in ('linux', 'macosx', 'windows'):
            return True
        return False

    def init_vertical_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            # self.line = Line(points = [100, 0, 100, 100])
            for i in range(0, self.V_NB_LINES):
                self.vertical_lines.append(Line())

    def update_vertical_lines(self):
        central_line_x = int(self.width/2)
        spacing = self.V_LINES_SPACING * self.width
        # self.line.points = [center_x, 0, center_x, 100]
        offset = -int(self.V_NB_LINES/2) + 0.5
        for i in range(0, self.V_NB_LINES):
            line_x = int(central_line_x + offset*spacing + self.current_offset_x)
            # line_y = i * spacing_y - self.current_offset_y
            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)
            self.vertical_lines[i].points = [x1, y1, x2, y2]
            offset += 1

    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            # self.line = Line(points = [100, 0, 100, 100])
            for i in range(0, self.H_NB_LINES):
                self.horizontal_lines.append(Line())

    def update_horizontal_lines(self):

        central_line_x = int(self.width / 2)
        spacing = self.V_LINES_SPACING * self.width
        # self.line.points = [center_x, 0, center_x, 100]
        offset = -int(self.V_NB_LINES / 2) + 0.5

        xmin = central_line_x+offset*spacing + self.current_offset_x
        xmax = central_line_x-offset*spacing + self.current_offset_x
        spacing_y = self.H_LINES_SPACING * self.height

        for i in range(0, self.H_NB_LINES):
            line_y = i * spacing_y - self.current_offset_y
            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)
            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def update(self, dt):
        time_factor = dt * 60
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.current_offset_y += self.speed * time_factor
        self.current_offset_x += self.current_speed_x * time_factor
        spacing_y = self.H_LINES_SPACING * self.height
        # spacing_x = self.V_LINES_SPACING * self.width
        if self.current_offset_y >= spacing_y:
            self.current_offset_y -= spacing_y
            # self.current_offset_x -= spacing_x SALTO DE LINEAS VERTICALES
        # print("dt: " + str(dt * 60))


class GalaxyApp(App):
    pass


GalaxyApp().run()