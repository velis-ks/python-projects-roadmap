# 🍳 Recipe Scaler CLI

A professional command-line interface (CLI) application designed for the hospitality industry. This tool dynamically scales recipe ingredients, calculates exact batch yields, and computes food costs by factoring in realistic ingredient waste percentages.

## 🚀 Features

* **Dynamic Scaling:** Instantly calculates multipliers based on target vs. base portions.
* **Waste Processing (Merma):** Automatically processes gross weights into net consumable weights based on custom waste percentages per ingredient.
* **Smart Cost Calculation:** Distinguishes between items priced by weight (per kilo) and items priced by unit (e.g., eggs).
* **JSON Data Model:** Uses a clean, isolated JSON database for easy recipe management and system updates.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Libraries:** `argparse`, `json`, `pathlib`, `sys` (Standard Library only, zero external dependencies).

## 💻 Installation & Usage

1. Clone the repository and navigate to the project directory:
   ```bash
   cd level-01-automation/03-recipe-scaler

2. Run the help command to view available arguments:
    ```bash
    python3 src/main.py --help

3. Scale a recipe by providing the exact dictionary key and target portions:
    ```bash
    python3 src/main.py --recipe tortilla_patatas --portions 150
