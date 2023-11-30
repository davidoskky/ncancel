#!/usr/bin/env python
import curses
import subprocess
import threading
import time
import queue

def init_curses():
    hide_cursor()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

def hide_cursor():
    curses.curs_set(0)


def fetch_jobs(job_queue):
    """Fetch job list from squeue in a separate thread."""
    while True:
        try:
            jobs = subprocess.check_output(['squeue']).decode().splitlines()
        except subprocess.CalledProcessError:
            jobs = ["Error: Unable to fetch jobs"]
        job_queue.put(jobs)
        time.sleep(2)  # Sleep for 2 seconds before fetching again

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
    last_jobs = []
    job_queue = queue.Queue()
    threading.Thread(target=fetch_jobs, args=(job_queue,), daemon=True).start()

    while True:
        stdscr.clear()

        # Display header
        stdscr.addstr("Ncancel - Slurm Job Manager\n", curses.A_BOLD)

        if not job_queue.empty():
            last_jobs = job_queue.get_nowait()

        if last_jobs:
            display_jobs(stdscr, last_jobs, current_line)

        stdscr.timeout(1000)  # 1 second

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
