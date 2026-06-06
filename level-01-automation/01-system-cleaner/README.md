# Level 1: Linux System Cleaner

An automated utility script designed to safely clean up temporary files, caches, and user trash in Debian/Ubuntu-based environments, preventing disk degradation and freeing up space.

## Features
* **Cache Management:** Scans `~/.cache` and selectively removes files and directories that have not been modified in the last 14 days.
* **Trash Disposal:** Completely empties the `~/.local/share/Trash/files` directory.
* **Failsafe Execution:** Requires explicit user confirmation before any deletion occurs.
* **Activity Logging:** Provides real-time terminal output of deleted items and calculates the total disk space freed in Megabytes (MB).

## Tech Stack
* **Language:** Python 3.x
* **Libraries:** `pathlib` (Object-oriented filesystem paths), `shutil` (High-level file operations), `logging`.

## How to Run

Since this script utilizes only the Python Standard Library, no virtual environment or external package installation is required.

1. Clone the repository and navigate to this project folder:
   ```bash
   cd level-01-automation/01-system-cleaner