#!/usr/bin/env python
import curses
import queue
import subprocess
import threading
import time


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
            jobs = subprocess.check_output(["squeue"]).decode().splitlines()
        except subprocess.CalledProcessError:
            jobs = ["Error: Unable to fetch jobs"]
        job_queue.put(jobs)
        time.sleep(2)  # Sleep for 2 seconds before fetching again


def get_work_dir(job_id):
    """Get the working directory for a given job ID using scontrol."""
    try:
        # Execute the scontrol command to get job details
        output = subprocess.check_output(
            ["scontrol", "show", "job", job_id], stderr=subprocess.STDOUT
        ).decode("utf-8")

        # Iterate over each line of the output
        for line in output.splitlines():
            # Check if the line contains the WorkDir information
            if line.strip().startswith("WorkDir="):
                # Extract and return the WorkDir path
                return line.strip().split("WorkDir=")[1]
    except subprocess.CalledProcessError as e:
        print(f"Error fetching work directory for job {job_id}: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    # Return empty string if WorkDir could not be found or in case of an error
    return None


def display_jobs(stdscr, job_lines, current_line):
    """Display the job list."""

    max_y, _ = stdscr.getmaxyx()
    max_job_line_index = max_y - 3
    work_dir = ""

    if job_lines:
        # Extract job ID from the currently selected line
        job_id = job_lines[current_line].split()[0]
        # Fetch the working directory for the current job
        work_dir = get_work_dir(job_id) or "Not available"

    for i, job in enumerate(job_lines[:max_job_line_index]):
        if i == current_line:
            stdscr.addstr(i, 0, job, curses.color_pair(1))
        else:
            stdscr.addstr(i, 0, job)

    # Display the working directory on the last line
    stdscr.move(max_y - 2, 0)
    stdscr.clrtoeol()
    stdscr.addstr(max_y - 1, 0, f"WorkDir: {work_dir}")


def cancel_job(job_id):
    """Cancel a job using scancel."""
    try:
        subprocess.call(["scancel", job_id])
    except subprocess.CalledProcessError:
        pass  # Add error handling if needed


def main(stdscr):
    init_curses()

    current_line = 1
    job_lines = []
    job_queue = queue.Queue()
    threading.Thread(target=fetch_jobs, args=(job_queue,), daemon=True).start()

    while True:
        stdscr.clear()

        # Display header
        stdscr.addstr("Ncancel - Slurm Job Manager\n", curses.A_BOLD)

        if not job_queue.empty():
            job_lines = job_queue.get_nowait()

        if job_lines:
            display_jobs(stdscr, job_lines, current_line)

        stdscr.timeout(1000)  # 1 second

        k = stdscr.getch()
        if k == curses.KEY_DOWN and current_line < len(job_lines) - 1:
            current_line = min(current_line + 1, len(job_lines))
        elif k == curses.KEY_UP and current_line > 0:
            current_line = max(current_line - 1, 1)
        elif k == ord("d"):  # 'd' for delete
            job_id = job_lines[current_line].split()[0]
            cancel_job(job_id)
        elif k == ord("q") or k == ord("Q"):
            break
        stdscr.refresh()


curses.wrapper(main)
