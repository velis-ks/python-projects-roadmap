"""
Recipe Scaler V2 - Database Integration Module
----------------------------------------------
This script connects to a local MySQL database (recipe_aid) to fetch
recipe ingredients, locations, and costs. It then scales the quantities
dynamically based on the requested number of portions.

Usage Example:
    python3 src/main.py --recipe "Spaghetti Carbonara" --portions 45
"""

import argparse
import sys
import mysql.connector
from mysql.connector import Error

def fetch_recipe_data(recipe_name: str):
    """
    Connects to the XAMPP MySQL database and fetches the recipe data
    using a multi-table JOIN query.

    Args:
        recipe_name (str): The exact name of the recipe in the database.

    Returns:
        list[dict]: A list of dictionaries containing the ingredient rows.
                    Returns None if a database error occurs.
    """
    try:
        # 1. Initialize the database connection
        connection = mysql.connector.connect(
            host='localhost',
            database='recipe_aid',
            user='root',
            password=''
        )
        
        if connection.is_connected():
            # 2. Create cursor (dictionary=True ensures rows behave like the old JSON format)
            cursor = connection.cursor(dictionary=True)
            
            # The SQL query linking recipes, recipe_ingredients, ingredients, and locations
            query = """
            SELECT 
                r.name AS recipe_name, 
                r.base_portions, 
                i.name AS ingredient_name, 
                l.location_name, 
                ri.gross_weight_gr, 
                i.waste_percentage, 
                i.cost_per_kilo
            FROM recipes r
            JOIN recipe_ingredients ri ON r.id = ri.recipe_id
            JOIN ingredients i ON ri.ingredient_id = i.id
            JOIN locations l ON i.location_id = l.id
            WHERE r.name = %s;
            """
            
            # 3. Execute the SQL query safely with parameterized inputs to prevent injection
            cursor.execute(query, (recipe_name,))
            
            # 4. Fetch the results
            records = cursor.fetchall()
            return records

    except Error as e:
        print(f"Database Error: {e}")
        sys.exit(1)
        
    finally:
        # 5. Close cursor and connection to prevent database lockups/memory leaks
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def main():
    """
    Main CLI execution logic. Parses terminal arguments, fetches data,
    calculates the scaled weights and costs, and prints the output.
    """
    # Set up the argument parser for terminal inputs
    parser = argparse.ArgumentParser(description="Recipe Scaler V2 (MySQL Edition)")
    parser.add_argument("-r", "--recipe", required=True, type=str, help="Name of the recipe in the DB")
    parser.add_argument("-p", "--portions", required=True, type=int, help="Target number of portions")
    args = parser.parse_args()

    # Fetch data by passing the CLI argument into the function
    db_records = fetch_recipe_data(args.recipe)
    
    if not db_records:
        print(f"Error: Recipe '{args.recipe}' not found in the database.")
        sys.exit(1)

    # Calculate the scaling multiplier using the first row's base portions
    base_portions = db_records[0]['base_portions']
    multiplier = args.portions / base_portions
    
    print(f"\nScaling '{args.recipe}' from {base_portions} to {args.portions} portions.")
    print(f"Multiplier: {multiplier}x")
    print("-" * 50)

    total_cost = 0.0

    # Process the math for each ingredient row returned by the database
    for row in db_records:
        ingredient = row['ingredient_name']
        location = row['location_name']
        waste_pct = float(row['waste_percentage'])
        cost_per_kilo = float(row['cost_per_kilo'])
        
        # Math logic: scale weight, apply waste percentage, calculate cost
        scaled_gross_gr = float(row['gross_weight_gr']) * multiplier
        scaled_net_gr = scaled_gross_gr * (1 - (waste_pct / 100))
        item_cost = (scaled_gross_gr / 1000) * cost_per_kilo
        
        total_cost += item_cost

        print(f"{ingredient} (Loc: {location})")
        print(f"Gross: {scaled_gross_gr:.2f}g | Net: {scaled_net_gr:.2f}g | Cost: €{item_cost:.2f}")
        print("-" * 50)

    # Calculate final batch and portion costs
    cost_per_portion = total_cost / args.portions

    print(f"Total Batch Cost: €{total_cost:.2f}")
    print(f"Cost Per Portion: €{cost_per_portion:.2f}")
    print("-" * 50 + "\n")

if __name__ == "__main__":
    main()