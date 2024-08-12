import sqlite3
from sqlite3 import Error

DATABASE_NAME = "inventory.db"

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(f"Error creating table: {e}")

def init_db():
    products_table = """ CREATE TABLE IF NOT EXISTS products (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            description TEXT,
                            price REAL NOT NULL,
                            quantity INTEGER NOT NULL
                        ); """

    conn = create_connection()

    if conn is not None:
        create_table(conn, products_table)
        conn.close()
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    init_db()