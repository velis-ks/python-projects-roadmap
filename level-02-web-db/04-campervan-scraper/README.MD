# 🚐 Campervan Price Tracker (eBay Stealth Scraper)

A robust, terminal-based CLI application designed to automate the extraction and filtering of vehicle listings from eBay. Built specifically to bypass modern Web Application Firewalls (WAFs) using stealth browser automation, filtering target vehicles (e.g., Mazda Bongo, VW T4/T5), and providing interactive OS-level notifications.

## 🏗️ Architecture & Tech Stack

- **Python 3.14+**: Core runtime environment.
- **Undetected-ChromeDriver**: Native browser automation that patches hex signatures in memory to evade enterprise WAF deep-inspection (bypassing 403/500 Captcha blocks).
- **BeautifulSoup4**: HTML node extraction and DOM parsing.
- **Rich**: Advanced terminal UI rendering with clickable hyperlink support.
- **Subprocess (`notify-send`)**: Native Linux desktop notifications.
- **Monkeypatching**: Dynamic runtime module injection for legacy dependency support.

## ✨ Key Features

1. **Dual Execution Modes**: 
   - **CLI Flags**: Pass arguments directly (e.g., `--query`, `--max-price`) for automated `cron` execution.
   - **Interactive Wizard**: Fallback UI that prompts the user step-by-step if no flags are provided.
2. **Stealth Mode**: Leverages local Chrome binaries via Selenium, stripping `navigator.webdriver` flags to mimic authentic human traffic.
3. **Smart Filtering**: Automatically drops junk listings, accessory parts, and sponsored ads by strictly evaluating keyword combinations.
4. **Clean File System**: Implements strict `try...finally` garbage collection to ensure temporary HTML dumps are purged from the drive after parsing.

## 🚀 Installation

Ensure you are running this on a Debian/Ubuntu environment with a local installation of Google Chrome.

1. Clone the repository and navigate to the directory:
   ```bash
   cd 04-campervan-scraper
Activate your virtual environment:

```bash
source .venv/bin/activate
Install the required dependencies:
```

```bash
pip install -r requirements.txt
```
💻 Usage
Interactive Mode:
Simply run the script without arguments to launch the step-by-step wizard.

```bash
python3 ebay_scraper.py
```
Automated CLI Mode:
Pass your search query and budget threshold directly into the terminal.

```bash
python3 ebay_scraper.py --query "Mazda Bongo campervan" --max-price 5000
python3 ebay_scraper.py --query "VW T4 campervan" --max-price 4000
```

📂 Project Structure
ebay_scraper.py: The main orchestrator. Handles CLI inputs, triggers the downloader, parses the DOM, applies business logic filters, and renders the Rich terminal UI.

html_downloader.py: The network bypass module. Manages the headless browser lifecycle, injects WAF-evasion scripts, and safely dumps the raw HTML to the local disk.

requirements.txt: Environment dependencies.