import sqlite3

# Connect to a database (or create one if it doesn't exist)
conn = sqlite3.connect("database.db")

# Create a cursor object
cursor = conn.cursor()

# Seeder Data
shirts = [
    ('t-shirt',"s1.png", "green", "S", 19.99, 10,'Recommend Skin Tone - Cool , Warn , Nature'),
    ('t-shirt',"s2.png","blue", "M", 29.99, 5, 'Recommend Skin Tone -  Nature'),
    ('t-shirt',"s3.png", "red", "L", 39.99, 3,'Recommend Skin Tone - Warn , Nature'),

    ('PVTS',"S4.png","pink", "S", 19.99, 10,'Recommend Skin Tone - Cool , Warn , Nature'),
    ('PVTS',"S5.png","white", "M", 29.99, 5, 'Recommend Skin Tone -  Nature'),
    ('PVTS',"S6.png","yellow", "L", 39.99, 3,'Recommend Skin Tone - Warn , Nature'),

    ('shirt',"S7.png","gray", "S", 19.99, 10,'Recommend Skin Tone - Cool , Warn , Nature'),
    ('shirt',"S8.png","plaid_pattern", "M", 29.99, 5, 'Recommend Skin Tone -  Nature'),

]

# Create shirts table
def create_table(cursor):

    # Drop table
    cursor.execute("DROP TABLE IF EXISTS shirts")

    # Create a table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shirts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        brand TEXT,
        path TEXT,
        color INTEGER,
        size TEXT,
        price FLOAT,
        stock INTEGER,
        suggestion TEXT          
    )
    """)

    conn.commit()

# Insert Shirt data
def insert_shirt(cursor,shirts):

    for shirt in shirts:
        cursor.execute(f"""
        INSERT INTO shirts (brand, path, color, size, price, stock, suggestion)
        VALUES {shirt}
        """)
    conn.commit()

# Fetch Shirt data
def fetch_shirts(cursor):
    cursor.execute("SELECT * FROM shirts")
    return cursor.fetchall()


def main():
    global conn, cursor, shirts

    create_table(cursor=cursor)
    insert_shirt(cursor=cursor, shirts=shirts)
    shirts = fetch_shirts(cursor=cursor)
    print(shirts)

    # Close the connection
    conn.close()

if __name__ == "__main__":
    main()