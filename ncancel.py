#!/usr/bin/env python
import curses
import subprocess

def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()  # Clear the screen

    current_line = 1  # Current line position in job list
    num_lines = curses.LINES - 4    

    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    while True:
        stdscr.clear()
        # Display header
        stdscr.addstr("Slurm Job Manager\n", curses.A_BOLD)
        # Fetch and display jobs
        jobs = subprocess.check_output(['squeue']).decode()
        job_lines = jobs.splitlines()

        for i in range(len(job_lines)):
            if i == current_line:
                stdscr.addstr(job_lines[i] + '\n', curses.color_pair(1))
            else:
                stdscr.addstr(job_lines[i] + '\n')

        k = stdscr.getch()
        if k == curses.KEY_DOWN and current_line < len(job_lines) - 1:
            current_line = min(current_line + 1, len(job_lines))
        elif k == curses.KEY_UP and current_line > 0:
            current_line = max(current_line - 1, 1)
        elif k == ord('d'):  # Example: 'd' for delete
            job_id = job_lines[current_line].split()[0]
            subprocess.call(['scancel', job_id])
        stdscr.refresh()
        # Other logic

curses.wrapper(main)
