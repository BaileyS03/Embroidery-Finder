import sqlite3

def print_all_items():
    # Connect to the SQLite database
    conn = sqlite3.connect('central_database.db')
    cursor = conn.cursor()

    # Execute a SELECT query to retrieve all items
    cursor.execute('SELECT * FROM items')

    # Fetch all rows
    rows = cursor.fetchall()

    # Print the header
    print("ID | Company | Set Title | Item Title | Image URL | Price | Set Price | Item URL")

    # Print each row
    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]:.4} | {row[5]} | {row[6]} | {row[7]:.4}")

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    print_all_items()
