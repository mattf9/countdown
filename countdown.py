#!/usr/bin/env python

import curses
import time

COUNTDOWN_MINUTES = 2


def countdown(minutes):
    seconds = 59
    minutes -= 1
    stdscr = curses.initscr()
    curses.curs_set(False)
    while (minutes >= 0) and (seconds >= 0):
        stdscr.addstr(
            0, 0, "Time Remaining: {:02d}:{:02d}".format(minutes, seconds))
        stdscr.refresh()
        time.sleep(1)
        seconds -= 1
        if seconds < 0:
            minutes -= 1
            seconds = 59
    curses.curs_set(True)
    curses.endwin()
    print('\nTask complete\n')


if __name__ == '__main__':
    countdown(COUNTDOWN_MINUTES)
