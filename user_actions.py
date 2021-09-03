from kivy.uix.relativelayout import RelativeLayout


def keyboard_closed(self):
    self._keyboard_unbind(on_key_down=self._on_keyboard_down)
    self._keyboard = None


def on_keyboard_down(self, keyboard, keycode, test, modifiers): # noqa
    if keycode[1] == 'left':
        self.current_speed_x = self.SPEED_X
    elif keycode[1] == 'right':
        self.current_speed_x = -self.SPEED_X
    elif keycode[1] == 'm':
        if self.mute:
            if self.audio: self.bgm_begin.volume = self.vol # noqa
            self.mute = False
        else:
            old_vol = self.vol
            if self.audio:
                # TODO: Put into fade functions
                # for self.vol in np.arange(start=1, stop=0, step=-0.1):
                #   self.vol = float(round(self.vol, 2))
                #   if self.audio: self.bgm_begin.volume = self.vol # noqa
                self.bgm_begin.volume = 0 # noqa
            self.vol = old_vol
            self.mute = True
    elif keycode[1] == 'd':
        self.on_debug_button_pressed()
    elif keycode[1] == 's':
        self.on_menu_button_pressed()
    elif keycode[1] == 'q':
        self.end_game()
    return True


def on_keyboard_up(self, keyboard, keycode): # noqa
    self.current_speed_x = 0
    return True


def on_touch_down(self, touch):
    if not self.state_game_over and self.state_game_started:
        if touch.x < self.width / 2:
            self.current_speed_x = self.SPEED_X
        else:
            self.current_speed_x = -self.SPEED_X
    return super(RelativeLayout, self).on_touch_down(touch)


def on_touch_up(self, touch): # noqa
    self.current_speed_x = 0
