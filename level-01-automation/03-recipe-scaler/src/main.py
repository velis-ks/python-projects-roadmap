import json
import argparse
import sys
from pathlib import Path

# Use __file__ so the script dynamically finds its own location
BASE_DIR = Path(__file__).resolve().parent
RECIPES_FILE = BASE_DIR / "recipes.json"

def load_recipes() -> dict:
    """Opens the JSON file and converts it into a Python dictionary."""
    
    # Add a safety check in case the file gets deleted or moved
    if not RECIPES_FILE.exists():
        print(f"Error: Database not found at {RECIPES_FILE}")
        sys.exit(1)
        
    # Open the actual file variable in read mode
    with open(RECIPES_FILE, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
            return data
        except json.JSONDecodeError as error:
            print(f"Error: Invalid JSON format. {error}")
            sys.exit(1)

def calculate_scaling(recipe_key: str, target_portions: int, data: dict) -> None:
    """Calculates exact ingredient amounts and costs based on the desired portions."""
    
    recipes = data.get("recipes", {})
    
    # 1. Check if the recipe exists in the database
    if recipe_key not in recipes:
        print(f"Error: Recipe '{recipe_key}' not found.")
        sys.exit(1)
        
    # 2. Extract specific recipe and base portions
    recipe = recipes[recipe_key]
    base_portions = recipe.get("base_portions", 1)
    
    # 3. Calculate multiplier
    multiplier = target_portions / base_portions
    
    print(f"Scaling '{recipe['name']}' from {base_portions} to {target_portions} portions.")
    print(f"Multiplier: {multiplier}x")
    print("-" * 30)

    ingredients = recipe.get("ingredients", [])
    total_recipe_cost = 0.0

    for item in ingredients:
        name = item.get("name")
        base_weight = item.get("gross_weight_gr")
        
        # Calculate scaled gross weight
        scaled_gross_weight = multiplier * base_weight

        # Calculate scaled net weight (subtracting waste)
        waste_percentage = item.get("waste_percentage")
        scaled_net_weight = scaled_gross_weight * (1 - (waste_percentage / 100))
        
        # Calculate cost
        base_price = item.get("cost_per_kilo")
        if "Unit" in name:
            item_cost = scaled_gross_weight * base_price
        else:
            item_cost = (scaled_gross_weight / 1000) * base_price
        
        # Accumulate total cost
        total_recipe_cost += item_cost
        
        # Print ingredient row
        print(f"{name} | Gross: {scaled_gross_weight:.2f}g | Net: {scaled_net_weight:.2f}g | Cost: {item_cost:.2f} €")
        print("-" * 30)

    # Calculate final portion cost
    cost_per_portion = total_recipe_cost / target_portions      
    
    # Print totals
    print(f"Total Batch Cost: €{total_recipe_cost:.2f}")  
    print(f"Cost Per Portion: €{cost_per_portion:.2f}") 
    print("-" * 30)


def main() -> None:
    # 1. Initialize the Argument Parser
    parser = argparse.ArgumentParser(description="Recipe Scaler CLI")
    
    # 2. Define the expected flags
    parser.add_argument("-r", "--recipe", type=str, required=True, help="Recipe ID")
    parser.add_argument("-p", "--portions", type=int, required=True, help="Target portions")
    
    # 3. Parse the command line inputs into the 'args' variable
    args = parser.parse_args()
    
    # 4. Load the database
    database = load_recipes()

    # 5. Execute the business logic using the variables from argparse
    calculate_scaling(args.recipe, args.portions, database)

# 6. The Execution Trigger (Flush to the left)
if __name__ == "__main__":
    main()
