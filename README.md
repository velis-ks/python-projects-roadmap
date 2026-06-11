# 🐍 Python & JS Projects Roadmap

Welcome to my development and automation repository. 

As a Full Stack Developer with a background in Java, PHP, and React, my absolute focus right now is on mastering **Python** and **JavaScript**. I am using this space to solidify my skills in system scripting, automation architecture, and modern full-stack development.

## 📂 Repository Structure

This roadmap is divided into different levels of complexity. Currently working on:

### Level 01: Automation & System Scripting (Python)
Scripts designed to interact directly with the operating system, manage hardware, and automate maintenance tasks.

* **[01-system-cleaner](./level-01-automation/01-system-cleaner):** A Python utility designed to automate deep cleaning, manage system caches, and empty the trash to optimize disk space.
* **[02-battery-monitor](./level-01-automation/02-battery-monitor):** A system utility written in Python to manage battery charge thresholds at the kernel level and dynamically configure CPU governors using TLP.
* **[03-recipe-scaler-v1](./level-01-automation/03-recipe-scaler-v1):** A professional Python CLI tool using `argparse` to parse JSON databases, calculate gross/net ingredient weights, and compute financial costs per portion for the hospitality sector.
* **[03-recipe-scaler-v2](./level-01-automation/03-recipe-scaler-v2):** The architectural evolution of the recipe scaler, migrating from static JSON files to a fully relational **MySQL** database. Features complex `JOIN` queries, parameterized inputs for security against SQL Injection, and strict execution within a `venv` to comply with PEP 668.

### Level 02: Web Automation, Scraping & Databases (Python)
Transitioning from local OS tools to external web architecture, data extraction, and embedded relational storage.

* **`04-campervan-scraper`**: A stealth web scraper and CLI tool built to bypass enterprise WAFs and track campervan prices (Mazda Bongo, VW T4/T5) on eBay. Engineered with Selenium, `undetected-chromedriver`, BeautifulSoup4, and Rich for an interactive terminal UI. Features dynamic argument parsing and strict garbage collection.
* **`05-todo-sqlite`**: *(In Progress)* Exploring embedded relational databases using Python's native `sqlite3`. Focusing on OOP connection managers, parameterized CRUD operations, and safe schema initialization.

## 🎯 Learning Objectives
* Deepening expertise in the Python ecosystem and virtual environments.
* System file manipulation (`/sys/`, `/etc/`) and hardware-level scripting.
* Relational database architecture, data normalization, and complex SQL integrations.
* Designing decoupled REST APIs to serve modern JavaScript frontends.
* Writing clean, modular, and well-documented code for production environments.

## 👨‍💻 Author
**Velis** - *Full Stack Developer & Linux Enthusiast*