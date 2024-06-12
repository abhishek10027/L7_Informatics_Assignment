import sqlite3

def create_database():
    conn = sqlite3.connect('ice_cream_parlor.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS seasonal_flavors (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        price REAL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ingredient_inventory (
        id INTEGER PRIMARY KEY,
        name TEXT,
        quantity INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_type TEXT,
        item_id INTEGER
    )
    ''')

    conn.commit()
    conn.close()
