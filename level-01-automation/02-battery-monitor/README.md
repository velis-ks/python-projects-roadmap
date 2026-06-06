# Linux Battery & Power Monitor

A Python automation script designed for low-level management of battery charge thresholds and CPU performance profiles on Linux systems (optimized for Lenovo ThinkPads).

## 🚀 Features

* **Battery Protection:** Directly modifies hardware files (`/sys/class/power_supply/BAT0/`) to limit charging (e.g., 25% - 80%), prolonging battery lifespan.
* **CPU Management:** Dynamically detects and applies the most optimal CPU governor (`schedutil` or `ondemand`).
* **TLP Integration:** Automatically generates and applies persistent power configurations in `/etc/default/tlp`.
* **Security & Notifications:** Includes `root` privilege verification, safe subprocess handling, and routes notifications to the active user's desktop environment (DBUS workaround).

## 🛠️ Technologies

* **Language:** Python 3 (Standard Library: `os`, `sys`, `subprocess`, `pathlib`)
* **System Dependencies:** `tlp`, `tlp-rdw`, `cpufrequtils`

## ⚙️ Usage

The script requires superuser privileges to modify kernel files and manage `systemd` services.

```bash
# Execute from the project root directory
sudo python3 src/main.py