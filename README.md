# Ncancel - Slurm Job Manager

## Introduction
Ncancel is a Python-based terminal application for managing Slurm jobs. It uses the `curses` library to provide a user-friendly, interactive interface for monitoring and managing jobs submitted to a Slurm workload manager. This tool simplifies the process of job management by allowing users to view, refresh, and cancel jobs directly from the terminal.

## Installation

### Prerequisites
- Python 3.x
- Access to a system running Slurm Workload Manager

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/davidoskky/ncancel.git
   ```
2. Link the script to your local binary folder 
    ```bash
    ln -s ncancel/ncancel.py ~/.local/bin/ncancel
    ```

## Key Commands
Arrow Up/Down: Navigate through the job list.
D: Cancel the selected job.
Q: Quit the application.

## Features
Real-Time Updates: The job list is automatically refreshed every 2 seconds.
Job Cancellation: Cancel jobs directly from the interface.
Error Handling: Displays errors (e.g., unable to fetch jobs).
