import sqlite3

def add_to_cart(item_type, item_id):
    conn = sqlite3.connect('ice_cream_parlor.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO cart (item_type, item_id) VALUES (?, ?)
    ''', (item_type, item_id))
    conn.commit()
    conn.close()

def Input_data():
    conn = sqlite3.connect('ice_cream_parlor.db')
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM seasonal_flavors')
    if cursor.fetchone()[0] == 0:
        seasonal_flavors = [
            (1, 'Vanilla Delight', 'Classic vanilla ice cream', 35.0),
            (2, 'Chocolate Heaven', 'Rich chocolate ice cream', 40.0),
            (3, 'Strawberry Surprise', 'Fresh strawberry ice cream', 38.0),
            (4, 'Minty Fresh', 'Cool mint ice cream', 36.0),
            (5, 'Caramel Crunch', 'Caramel ice cream with crunchy bits', 42.0),
            (6, 'Cookies and Cream', 'Cookies and cream ice cream', 45.0),
            (7, 'Pistachio Paradise', 'Pistachio flavored ice cream', 40.0),
            (8, 'Mango Tango', 'Refreshing mango ice cream', 39.0),
            (9, 'Blueberry Bliss', 'Blueberry flavored ice cream', 41.0),
            (10, 'Lemon Zest', 'Tangy lemon ice cream', 37.0)
        ]
        cursor.executemany('''
        INSERT INTO seasonal_flavors (id, name, description, price) VALUES (?, ?, ?, ?)
        ''', seasonal_flavors)

    cursor.execute('SELECT COUNT(*) FROM ingredient_inventory')
    if cursor.fetchone()[0] == 0:
        ingredients = [
            (1, 'Milk', 100),
            (2, 'Sugar', 50),
            (3, 'Vanilla Extract', 20),
            (4, 'Cocoa Powder', 30),
            (5, 'Strawberries', 25),
            (6, 'Mint Leaves', 15),
            (7, 'Caramel', 10),
            (8, 'Cookies', 40),
            (9, 'Pistachios', 30),
            (10, 'Mangoes', 20),
            (11, 'Blueberries', 15),
            (12, 'Lemons', 10)
        ]
        cursor.executemany('''
        INSERT INTO ingredient_inventory (id, name, quantity) VALUES (?, ?, ?)
        ''', ingredients)

    conn.commit()
    conn.close()
