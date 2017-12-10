#!/usr/bin/env python

# Source: https://github.com/atizo/pygame/blob/master/examples/eventlist.py

"""Eventlist is a sloppy style of pygame, but is a handy
tool for learning about pygame events and input. At the
top of the screen are the state of several device values,
and a scrolling list of events are displayed on the bottom.

This is not quality 'ui' code at all, but you can see how
to implement very non-interactive status displays, or even
a crude text output control.
"""


import pygame


ImgOnOff = []
Font = None
LastKey = None


def showtext(win, pos, text, color, bgcolor):
    textimg = Font.render(text, 1, color, bgcolor)
    win.blit(textimg, pos)
    return pos[0] + textimg.get_width() + 5, pos[1]


def drawstatus(win):
    bgcolor = 50, 50, 50
    win.fill(bgcolor, (0, 0, 640, 120))
    win.blit(Font.render('Status Area', 1, (155, 155, 155), bgcolor), (2, 2))

    pos = showtext(win, (10, 30), 'Mouse Focus', (255, 255, 255), bgcolor)
    win.blit(ImgOnOff[pygame.mouse.get_focused()], pos)

    pos = showtext(win, (330, 30), 'Keyboard Focus', (255, 255, 255), bgcolor)
    win.blit(ImgOnOff[pygame.key.get_focused()], pos)

    pos = showtext(win, (10, 60), 'Mouse Position', (255, 255, 255), bgcolor)
    p = '%s, %s' % pygame.mouse.get_pos()
    pos = showtext(win, pos, p, bgcolor, (255, 255, 55))

    pos = showtext(win, (330, 60), 'Last Keypress', (255, 255, 255), bgcolor)
    if LastKey:
        p = '%d, %s' % (LastKey, pygame.key.name(LastKey))
    else:
        p = 'None'
    pos = showtext(win, pos, p, bgcolor, (255, 255, 55))

    pos = showtext(win, (10, 90), 'Input Grabbed', (255, 255, 255), bgcolor)
    win.blit(ImgOnOff[pygame.event.get_grab()], pos)


def drawhistory(win, history):
    win.blit(Font.render('Event History Area', 1, (155, 155, 155), (0,0,0)), (2, 132))
    ypos = 450
    h = list(history)
    h.reverse()
    for line in h:
        r = win.blit(line, (10, ypos))
        win.fill(0, (r.right, r.top, 620, r.height))
        ypos -= Font.get_height()


def cleanup():
    pygame.quit()


def main():
    pygame.init()

    win = pygame.display.set_mode((640, 480), pygame.RESIZABLE)
    pygame.display.set_caption("Mouse Focus Workout")

    global Font
    Font = pygame.font.Font(None, 26)

    global ImgOnOff
    ImgOnOff.append(Font.render("Off", 1, (0, 0, 0), (255, 50, 50)))
    ImgOnOff.append(Font.render("On", 1, (0, 0, 0), (50, 255, 50)))

    history = []

    #let's turn on the joysticks just so we can play with em
    for x in range(pygame.joystick.get_count()):
        j = pygame.joystick.Joystick(x)
        j.init()
        txt = 'Enabled joystick: ' + j.get_name()
        img = Font.render(txt, 1, (50, 200, 50), (0, 0, 0))
        history.append(img)
    if not pygame.joystick.get_count():
        img = Font.render('No Joysticks to Initialize', 1, (50, 200, 50), (0, 0, 0))
        history.append(img)

    going = True
    while going:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                going = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    going = False
                else:
                    global LastKey
                    LastKey = e.key
            if e.type == pygame.MOUSEBUTTONDOWN:
                pygame.event.set_grab(1)
            elif e.type == pygame.MOUSEBUTTONUP:
                pygame.event.set_grab(0)
            if e.type == pygame.VIDEORESIZE:
                win = pygame.display.set_mode(e.size, pygame.RESIZABLE)

            if e.type != pygame.MOUSEMOTION:
                txt = '%s: %s' % (pygame.event.event_name(e.type), e.dict)
                img = Font.render(txt, 1, (50, 200, 50), (0, 0, 0))
                history.append(img)
                history = history[-13:]


        drawstatus(win)
        drawhistory(win, history)

        pygame.display.flip()
        pygame.time.wait(10)

    cleanup()

if __name__ == '__main__':
    main()
