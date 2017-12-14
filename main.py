#!/usr/bin/env python

# Based on: https://github.com/atizo/pygame/blob/master/examples/eventlist.py

"""Eventlist is a sloppy style of pygame, but is a handy
tool for learning about pygame events and input. At the
top of the screen are the state of several device values,
and a scrolling list of events are displayed on the bottom.

This is not quality 'ui' code at all, but you can see how
to implement very non-interactive status displays, or even
a crude text output control.
"""


import pygame


FONT_SIZE = 26

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT

STATUS_AREA_RECT = 0, 0, WINDOW_WIDTH, 120
STATUS_AREA_LABEL_POS    = 2  , 2
MOUSE_FOCUS_LABEL_POS    = 10 , 30
KEYBOARD_FOCUS_LABEL_POS = 330, 30
MOUSE_POSITION_LABEL_POS = 10 , 60
LAST_KEYPRESS_LABEL_POS  = 330, 60
INPUT_GRABBED_LABEL_POS  = 10 , 90

HISTORY_LABEL_POS = 2, 132
HISTORY_BORDER_SIZE = 10
HISTORY_LINE_COUNT = 13

WHITE      = 255, 255, 255
LIGHTGREY  = 155, 155, 155
DARKGREY   = 50 , 50 , 50 
BLACK      = 0  , 0  , 0
RED        = 255, 50 , 50
YELLOW     = 255, 255, 55
LIGHTGREEN = 50 , 255, 50
DARKGREEN  = 50 , 200, 50

LOOP_PAUSE_TIME = 10  # ms


_switch_img = []
_font = None


class Status:
    def __init__(self, win):
        self.window = win
        self.lastkey = None
        self.update()

    def update(self):
        self.window.fill(DARKGREY, STATUS_AREA_RECT)
        self.window.blit(_font.render('Status Area', 1, LIGHTGREY, DARKGREY), STATUS_AREA_LABEL_POS)

        pos = showtext(self.window, MOUSE_FOCUS_LABEL_POS, 'Mouse Focus', WHITE, DARKGREY)
        self.window.blit(_switch_img[pygame.mouse.get_focused()], pos)

        pos = showtext(self.window, KEYBOARD_FOCUS_LABEL_POS, 'Keyboard Focus', WHITE, DARKGREY)
        self.window.blit(_switch_img[pygame.key.get_focused()], pos)

        pos = showtext(self.window, MOUSE_POSITION_LABEL_POS, 'Mouse Position', WHITE, DARKGREY)
        mousepos = "{}, {}".format(*pygame.mouse.get_pos())
        showtext(self.window, pos, mousepos, DARKGREY, YELLOW)

        pos = showtext(self.window, LAST_KEYPRESS_LABEL_POS, 'Last Keypress', WHITE, DARKGREY)
        if self.lastkey:
            lastkey = f"{self.lastkey}, {pygame.key.name(self.lastkey)}"
        else:
            lastkey = 'None'
        showtext(self.window, pos, lastkey, DARKGREY, YELLOW)

        pos = showtext(self.window, INPUT_GRABBED_LABEL_POS, 'Input Grabbed', WHITE, DARKGREY)
        self.window.blit(_switch_img[pygame.event.get_grab()], pos)


def showtext(win, pos, text, color, bgcolor):
    textimg = _font.render(text, True, color, bgcolor)
    win.blit(textimg, pos)
    return pos[0] + textimg.get_width() + 5, pos[1]


def drawhistory(win, history):
    fontheight = _font.get_height()
    win.blit(_font.render('Event History Area', True, LIGHTGREY, BLACK), HISTORY_LABEL_POS)
    ypos = WINDOW_HEIGHT - HISTORY_BORDER_SIZE - fontheight
    h = list(history)
    h.reverse()
    for line in h:
        r = win.blit(line, (HISTORY_BORDER_SIZE, ypos))
        win.fill(0, (r.right, r.top, WINDOW_WIDTH - HISTORY_BORDER_SIZE, r.height))
        ypos -= fontheight


def cleanup():
    pygame.quit()


def main():
    global _font
    global _switch_img

    pygame.init()

    win = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
    pygame.display.set_caption("Event List")

    _font = pygame.font.Font(None, FONT_SIZE)

    _switch_img.append(_font.render("Off", True, BLACK, RED))
    _switch_img.append(_font.render("On", True, BLACK, LIGHTGREEN))

    history = []
    status = Status(win)

    # Joysticks can be displayed only if they are initialized
    for i in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        txt = f'Enabled joystick: {joystick.get_name()}'
        img = _font.render(txt, True, DARKGREEN, BLACK)
        history.append(img)
    if pygame.joystick.get_count() == 0:
        img = _font.render('No Joysticks to Initialize', True, DARKGREEN, BLACK)
        history.append(img)

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
                win = pygame.display.set_mode(e.size, pygame.RESIZABLE)

            if e.type != pygame.MOUSEMOTION:
                txt = f"{pygame.event.event_name(e.type)}: {e.dict}"
                img = _font.render(txt, True, DARKGREEN, BLACK)
                history.append(img)
                history = history[-HISTORY_LINE_COUNT:]
                
        status.update()
        drawhistory(win, history)

        pygame.display.flip()
        pygame.time.wait(LOOP_PAUSE_TIME)

    cleanup()


if __name__ == '__main__':
    main()
