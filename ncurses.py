#!/usr/bin/env python
import curses
import subprocess

def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()  # Clear the screen
    while True:
        stdscr.clear()
        # Display header
        stdscr.addstr("Slurm Job Manager\n", curses.A_BOLD)
        # Fetch and display jobs
        jobs = subprocess.check_output(['squeue']).decode()
        stdscr.addstr(jobs)
        # Handle key presses for scrolling and selecting
        k = stdscr.getch()
        if k == curses.KEY_DOWN:
            stdscr.clear()
        elif k == curses.KEY_UP:
            stdscr.clear()
        elif k == ord('d'):  # Example: 'd' for delete
            stdscr.clear()
        # Refresh the screen
        stdscr.refresh()
        # Other logic

curses.wrapper(main)
