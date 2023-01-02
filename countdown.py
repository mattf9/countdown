#!/usr/bin/env python3

import argparse
import curses
import datetime
import sqlite3
import sys
import time


def countdown(minutes, description):
    original_minutes = minutes
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
            0, 0, "Time Remaining: {:02d}:{:02d}  {}".format(minutes, seconds, description))
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
                stdscr.addstr(1, 0, "              ")
            else:
                paused = True
                stdscr.addstr(1, 0, "*** PAUSED ***", curses.A_REVERSE)
                stdscr.refresh()
    end_curses()
    print('\nTask complete\n')
    save_task(original_minutes, description)


def save_task(minutes, description):
    sqliteConnection = sqlite3.connect('tasks.db')
    c = sqliteConnection.cursor()
    current_time = str(datetime.datetime.now())
    c.execute('''
             
                CREATE TABLE if not exists task_history(
                task_endtime TEXT,
                task_minutes INTEGER, 
                task_description TEXT
            )''')
    sql = ''' INSERT INTO task_history(task_endtime, task_minutes, task_description)
              VALUES(?,?,?) '''
    c.execute(sql, (current_time, minutes, description))
    sqliteConnection.commit()
    c.close()
    sqliteConnection.close()
    # pass

def end_curses():
    curses.curs_set(True)
    curses.nocbreak()
    curses.echo()
    curses.endwin()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(epilog="'p' to pause, space or 'q' to quit")
    parser.add_argument("-m", "--minutes", type=int, default=2, help = "set time to count down from")
    parser.add_argument("-d", "--description", default="", help = "description of task")
    args = parser.parse_args()
 
    countdown(args.minutes, args.description)
   
