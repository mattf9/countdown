#!/usr/bin/env python3

import argparse
import curses
import sys
import time


def countdown(minutes):
    paused = False
    seconds = 59
    minutes -= 1
    stdscr = curses.initscr()
    curses.curs_set(False)
    stdscr.nodelay(True)
    curses.noecho()
    curses.cbreak()
    while (minutes >= 0) and (seconds >= 0):
        stdscr.addstr(
            0, 0, "Time Remaining: {:02d}:{:02d}".format(minutes, seconds))
        stdscr.refresh()
        time.sleep(1)
        if not paused:
            seconds -= 1
        if seconds < 0:
            minutes -= 1
            seconds = 59
        c = stdscr.getch()
        if c == ord('q'):
            end_curses()
            sys.exit(0)
        if c == ord(' ') or c == ord('p'):
            if paused:
                paused = False
                stdscr.addstr(0, 0, "Time Remaining: {:02d}:{:02d}               ".format(minutes, seconds))
            else:
                paused = True
                stdscr.addstr(0, 0, "Time Remaining: {:02d}:{:02d} *** PAUSED ***".format(minutes, seconds),curses.A_REVERSE)
                stdscr.refresh()
    end_curses()
    print('\nTask complete\n')


def end_curses():
    curses.curs_set(True)
    curses.nocbreak()
    curses.echo()
    curses.endwin()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--minutes", type=int, default=2, help = "set time to count down from")
    args = parser.parse_args()
 
    countdown(args.minutes)
