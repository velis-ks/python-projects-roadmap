# Recipe Scaler V2

A CLI (Command Line Interface) tool developed in Python for managing and dynamically scaling recipes in professional hospitality environments. Version 2 abandons static JSON files in favor of a relational MySQL database architecture.

## Main Features

* **MySQL Integration:** Direct connection to a normalized database to manage recipes, ingredients, suppliers, and locations.
* **Waste % Calculation:** Automatically calculates the gross and net weight of each ingredient based on its waste percentage.
* **Dynamic Scaling:** Recalculates exact quantities, total batch cost, and cost per portion based on the target number of portions entered via the terminal.
* **SQL Injection Prevention:** Uses parameterized queries (`%s`) to protect database execution.

## Prerequisites

* Python 3.10+
* MySQL Server (e.g., XAMPP) running on `localhost`.

## Installation & Setup

Due to PEP 668 restrictions on modern Linux distributions (like Ubuntu), this project must be run inside an isolated virtual environment.

1. **Clone the repository and navigate to the folder:**
   ```bash
   cd 03-recipe-scaler-v2

2. Create and activate the virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt

## CLI Usage

The script is executed via the terminal by passing arguments using flags.

Command Structure:
    ```bash
    python3 src/main.py --recipe "Recipe Name" --portions <amount>

Usage Example:
    ```bash
    python3 src/main.py -r "Spaghetti Carbonara" -p 45

Arguments:
- -r or --recipe (Required): The exact name of the recipe as it appears in the database. (Enclose in quotes if it contains spaces).

- -p or --portions (Required): An integer representing the target number of portions to prepare.

## Database Structure (recipe_aid)

The project assumes a normalized database with the following core tables:
- recipes (id, name, base_portions, profit_margin)
- ingredients (id, name, waste_percentage, cost_per_kilo, location_id)
- recipe_ingredients (Pivot table: recipe_id, ingredient_id, gross_weight_gr)
- locations (id, location_name)