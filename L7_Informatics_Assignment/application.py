import sqlite3
from tabulate import tabulate
from add_values_to_database import add_to_cart, Input_data
from database import create_database

def search(keyword):
    conn = sqlite3.connect('ice_cream_parlor.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT 'Flavor' AS Type, id, name, description, price FROM seasonal_flavors
    WHERE name LIKE ? OR description LIKE ?
    UNION
    SELECT 'Ingredient' AS Type, id, name, quantity AS price FROM ingredient_inventory
    WHERE name LIKE ?
    ORDER BY name
    ''', ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))
    rows = cursor.fetchall()
    conn.close()
    return rows

def view_cart():
    conn = sqlite3.connect('ice_cream_parlor.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT cart.id, cart.item_type, seasonal_flavors.name, seasonal_flavors.price
    FROM cart
    JOIN seasonal_flavors ON cart.item_id = seasonal_flavors.id
    WHERE cart.item_type = 'flavor'
    UNION
    SELECT cart.id, cart.item_type, ingredient_inventory.name, ingredient_inventory.quantity
    FROM cart
    JOIN ingredient_inventory ON cart.item_id = ingredient_inventory.id
    WHERE cart.item_type = 'ingredient'
    ''')
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("Cart is empty.")
    else:
        print(tabulate(rows, headers=['Cart ID', 'Item Type', 'Name', 'Price/Quantity']))
        total_price = calculate_ice_cream_price()
        print(f"\nTotal Price of items in cart: RS: {total_price:.2f} /-")

def view_seasonal_flavors():
    conn = sqlite3.connect('ice_cream_parlor.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM seasonal_flavors')
    rows = cursor.fetchall()
    conn.close()
    return rows

def view_ingredients():
    conn = sqlite3.connect('ice_cream_parlor.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ingredient_inventory')
    rows = cursor.fetchall()
    conn.close()
    return rows

def calculate_ice_cream_price():
    conn = sqlite3.connect('ice_cream_parlor.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT SUM(seasonal_flavors.price) + SUM(ingredient_inventory.quantity)
    FROM cart
    LEFT JOIN seasonal_flavors ON cart.item_id = seasonal_flavors.id AND cart.item_type = 'flavor'
    LEFT JOIN ingredient_inventory ON cart.item_id = ingredient_inventory.id AND cart.item_type = 'ingredient'
    ''')
    total_price = cursor.fetchone()[0] or 0
    conn.close()
    return total_price

def main():
    while True:
        print("\nWelcome to the Ice Cream Parlor Cafe!")
        print("1. View Menu")
        print("2. Search")
        print("3. Add to Cart")
        print("4. View Cart")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            print("\nSeasonal Flavors:")
            flavors = view_seasonal_flavors()
            if flavors:
                print(tabulate(flavors, headers=['ID', 'Name', 'Description', 'Price']))
            else:
                print("No seasonal flavors available.")

            print("\nIngredients:")
            ingredients = view_ingredients()
            if ingredients:
                print(tabulate(ingredients, headers=['ID', 'Name', 'Price']))
            else:
                print("No ingredients available.")

        elif choice == '2':
            keyword = input("Enter keyword to search: ")
            results = search(keyword)
            if results:
                print("\nSearch Results:")
                print(tabulate(results, headers=['Type', 'ID', 'Name', 'Price']))
            else:
                print("No results found for the given keyword.")

        elif choice == '3':
            while True:
                print("\nSeasonal Flavors:")
                flavors = view_seasonal_flavors()
                if flavors:
                    print(tabulate(flavors, headers=['ID', 'Name', 'Description', 'Price']))
                else:
                    print("No seasonal flavors available.")
                    break
                
                flavor_id = input("Enter flavor ID to add to cart (or 'none' to finish adding flavors): ")
                if flavor_id.lower() == 'none':
                    break
                add_to_cart('flavor', int(flavor_id))
                print("Flavor added to cart successfully!")

            while True:
                print("\nIngredients:")
                ingredients = view_ingredients()
                if ingredients:
                    print(tabulate(ingredients, headers=['ID', 'Name', 'Price']))
                else:
                    print("No ingredients available.")
                    break

                ingredient_id = input("Enter ingredient ID to add to cart (or 'none' to finish adding ingredients): ")
                if ingredient_id.lower() == 'none':
                    break
                add_to_cart('ingredient', int(ingredient_id))
                print("Ingredient added to cart successfully!")

        elif choice == '4':
            view_cart()

        elif choice == '5':
            clear_cart()
            print("User input data cleared. Exiting...")
            break

        else:
            print("Invalid choice.")

def clear_cart():
    conn = sqlite3.connect('ice_cream_parlor.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cart')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    Input_data()
    main()
