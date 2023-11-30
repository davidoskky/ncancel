#!/usr/bin/env python
import curses
import subprocess
import threading
import queue

def init_curses():
    hide_cursor()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

def hide_cursor()
    curses.curs_set(0)

def fetch_jobs():
    """Fetch job list from squeue."""
    try:
        return subprocess.check_output(['squeue']).decode().splitlines()
    except subprocess.CalledProcessError:
        return ["Error: Unable to fetch jobs"]

def display_jobs(stdscr, job_lines, current_line):
    """Display the job list."""
    for i, job in enumerate(job_lines):
        if i == current_line:
            stdscr.addstr(job + '\n', curses.color_pair(1))
        else:
            stdscr.addstr(job + '\n')

def cancel_job(job_id):
    """Cancel a job using scancel."""
    try:
        subprocess.call(['scancel', job_id])
    except subprocess.CalledProcessError:
        pass  # Add error handling if needed

def main(stdscr):
    init_curses()

    current_line = 1
    job_queue = queue.Queue()
    threading.Thread(target=fetch_jobs, args=(job_queue,), daemon=True).start()

    while True:
        stdscr.clear()

        # Display header
        stdscr.addstr("Ncancel - Slurm Job Manager\n", curses.A_BOLD)

        if not job_queue.empty():
            jobs = job_queue.get_nowait()
        else:
            jobs = []

        display_jobs(stdscr, job_lines, current_line)

        stdscr.timeout(2000)  # 2 seconds

        k = stdscr.getch()
        if k == curses.KEY_DOWN and current_line < len(job_lines) - 1:
            current_line = min(current_line + 1, len(job_lines))
        elif k == curses.KEY_UP and current_line > 0:
            current_line = max(current_line - 1, 1)
        elif k == ord('d'):  # 'd' for delete
            job_id = job_lines[current_line].split()[0]
            cancel_job(job_id)
        stdscr.refresh()

curses.wrapper(main)
