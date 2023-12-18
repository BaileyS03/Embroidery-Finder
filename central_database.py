import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('central_database.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Create the items table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY,
        company TEXT NOT NULL,
        set_title TEXT NOT NULL,
        item_title TEXT NOT NULL,
        image_url TEXT,
        price REAL,
        set_price REAL,
        item_url TEXT
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
