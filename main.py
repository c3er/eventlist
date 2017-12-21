#!/usr/bin/env python

# Based on: https://github.com/atizo/pygame/blob/master/examples/eventlist.py
# As stated in the Pygame readme file (https://github.com/atizo/pygame/blob/master/readme.rst),
# the used example is licensed as public domain.

"""A handy tool for learning about pygame events and input.
At the top of the screen are the state of several device
values, and a scrolling list of events are displayed on the
bottom.
"""


import collections

import pygame


FONT_SIZE = 26

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT

STATUS_AREA_HEIGHT = 120
STATUS_AREA_LABEL_POS    = 2  , 2
MOUSE_FOCUS_LABEL_POS    = 10 , 30
MOUSE_FOCUS_INFO_POS     = 150, 30
MOUSE_POSITION_LABEL_POS = 10 , 60
MOUSE_POSITION_INFO_POS  = 150, 60
MOUSE_POSITION_INFO_POS  = 150, 60
INPUT_GRABBED_LABEL_POS  = 10 , 90
INPUT_GRABBED_INFO_POS   = 150, 90
KEYBOARD_FOCUS_LABEL_POS = 330, 30
KEYBOARD_FOCUS_INFO_POS  = 470, 30
LAST_KEYPRESS_LABEL_POS  = 330, 60
LAST_KEYPRESS_INFO_POS   = 470, 60

HISTORY_LABEL_POS = 2, 132
HISTORY_BORDER_SIZE = 10
HISTORY_LINE_COUNT = 17

AREA_LABEL_COLOR       = 155, 155, 155
STATUS_AREA_BGCOLOR    = 50 , 50 , 50
STATUS_LABEL_COLOR     = 255, 255, 255
STATUS_INFO_FONT_COLOR = 0  , 0  , 0
STATUS_INFO_BGCOLOR    = 255, 255, 55
ONSWITCH_BGCOLOR       = 50 , 255, 50
OFFSWITCH_BGCOLOR      = 255, 50 , 50
HISTORY_AREA_BGCOLOR   = 0  , 0  , 0
HISTORY_FONT_COLOR     = 50 , 200, 50

LOOP_PAUSE_TIME = 10  # ms


_switch_img = []
_font = None


class Status:
    def __init__(self, win):
        self.window = win
        self.lastkey = None
        self.update()

    def update(self):
        self.window.fill(
            STATUS_AREA_BGCOLOR,
            (0, 0, self.window.get_width(), STATUS_AREA_HEIGHT)
        )
        self.window.blit(
            _font.render('Status Area', 1, AREA_LABEL_COLOR, STATUS_AREA_BGCOLOR),
            STATUS_AREA_LABEL_POS
        )

        showtext(
            self.window,
            MOUSE_FOCUS_LABEL_POS,
            'Mouse Focus',
            STATUS_LABEL_COLOR,
            STATUS_AREA_BGCOLOR
        )
        self.window.blit(_switch_img[pygame.mouse.get_focused()], MOUSE_FOCUS_INFO_POS)

        showtext(
            self.window,
            MOUSE_POSITION_LABEL_POS,
            'Mouse Position',
            STATUS_LABEL_COLOR,
            STATUS_AREA_BGCOLOR
        )
        mousepos = "{}, {}".format(*pygame.mouse.get_pos())
        showtext(
            self.window,
            MOUSE_POSITION_INFO_POS,
            mousepos,
            STATUS_INFO_FONT_COLOR,
            STATUS_INFO_BGCOLOR
        )

        showtext(
            self.window,
            INPUT_GRABBED_LABEL_POS,
            'Input Grabbed',
            STATUS_LABEL_COLOR,
            STATUS_AREA_BGCOLOR
        )
        self.window.blit(_switch_img[pygame.event.get_grab()], INPUT_GRABBED_INFO_POS)

        showtext(
            self.window,
            KEYBOARD_FOCUS_LABEL_POS,
            'Keyboard Focus',
            STATUS_LABEL_COLOR,
            STATUS_AREA_BGCOLOR
        )
        self.window.blit(_switch_img[pygame.key.get_focused()], KEYBOARD_FOCUS_INFO_POS)

        showtext(
            self.window,
            LAST_KEYPRESS_LABEL_POS,
            'Last Keypress',
            STATUS_LABEL_COLOR,
            STATUS_AREA_BGCOLOR
        )
        if self.lastkey:
            lastkey = f"{self.lastkey}, {pygame.key.name(self.lastkey)}"
        else:
            lastkey = 'None'
        showtext(
            self.window,
            LAST_KEYPRESS_INFO_POS,
            lastkey,
            STATUS_INFO_FONT_COLOR,
            STATUS_INFO_BGCOLOR
        )


class History(collections.UserList):
    def __init__(self, win):
        super().__init__()
        self.window = win

    def draw(self):
        images = [
            _font.render(line, True, HISTORY_FONT_COLOR, HISTORY_AREA_BGCOLOR)
            for line in self.data[-HISTORY_LINE_COUNT:]
        ]
        fontheight = _font.get_height()
        self.window.blit(
            _font.render('Event History Area', True, AREA_LABEL_COLOR, HISTORY_AREA_BGCOLOR),
            HISTORY_LABEL_POS
        )
        ypos = WINDOW_HEIGHT - HISTORY_BORDER_SIZE - fontheight
        images.reverse()
        for img in images:
            r = self.window.blit(img, (HISTORY_BORDER_SIZE, ypos))
            self.window.fill(0, (r.right, r.top, WINDOW_WIDTH - HISTORY_BORDER_SIZE, r.height))
            ypos -= fontheight


def init_window(size):
    return pygame.display.set_mode(size, pygame.RESIZABLE)


def showtext(win, pos, text, color, bgcolor):
    textimg = _font.render(text, True, color, bgcolor)
    win.blit(textimg, pos)


def cleanup():
    pygame.quit()


def main():
    global _font
    global _switch_img

    pygame.init()

    win = init_window(WINDOW_SIZE)
    pygame.display.set_caption("Event List")

    _font = pygame.font.Font(None, FONT_SIZE)

    _switch_img.append(_font.render("Off", True, STATUS_INFO_FONT_COLOR, OFFSWITCH_BGCOLOR))
    _switch_img.append(_font.render("On", True, STATUS_INFO_FONT_COLOR, ONSWITCH_BGCOLOR))

    history = History(win)
    status = Status(win)

    # Joysticks can be displayed only if they are initialized
    for i in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        history.append(f'Enabled joystick: {joystick.get_name()}')
    if pygame.joystick.get_count() == 0:
        history.append('No Joysticks to Initialize')

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False
                else:
                    status.lastkey = e.key

            if e.type == pygame.MOUSEBUTTONDOWN:
                pygame.event.set_grab(True)
            elif e.type == pygame.MOUSEBUTTONUP:
                pygame.event.set_grab(False)

            if e.type == pygame.VIDEORESIZE:
                win = init_window(e.size)

            if e.type != pygame.MOUSEMOTION:
                history.append(f"{pygame.event.event_name(e.type)}: {e.dict}")

        status.update()
        history.draw()

        pygame.display.flip()
        pygame.time.wait(LOOP_PAUSE_TIME)

    cleanup()


if __name__ == '__main__':
    main()
