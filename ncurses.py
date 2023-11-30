#!/usr/bin/env python
import curses
import subprocess

def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()  # Clear the screen

    current_line = 0  # Current line position in job list
    num_lines = curses.LINES - 4    
    while True:
        stdscr.clear()
        # Display header
        stdscr.addstr("Slurm Job Manager\n", curses.A_BOLD)
        # Fetch and display jobs
        jobs = subprocess.check_output(['squeue']).decode()
        stdscr.addstr(jobs)

        for i in range(current_line, min(current_line + num_lines, len(job_lines))):
            stdscr.addstr(job_lines[i] + '\n')
        # Handle key presses for scrolling and selecting
        k = stdscr.getch()
        if k == curses.KEY_DOWN and current_line < len(job_lines) - num_lines:
            current_line += 1
        elif k == curses.KEY_UP and current_line > 0:
            current_line -= 1
        elif k == ord('d'):  # Example: 'd' for delete
            # Cancel job logic
            pass
        # Refresh the screen
        stdscr.refresh()
        # Other logic

curses.wrapper(main)
