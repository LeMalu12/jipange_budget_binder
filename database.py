import sqlite3


DATABASE = "jipange.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection

def seed_portfolios():
    connection = get_db_connection()

    starting_portfolios = [
        ("Rent", 50000),
        ("Electricity", 10000),
        ("Food", 10000),
        ("Transport", 5000),
        ("Savings", 10000),
        ("Flexible", 15000)
    ]

    for name, balance in starting_portfolios:
        connection.execute(
            """
            INSERT OR IGNORE INTO portfolios (name, balance)
            VALUES (?, ?)
            """,
            (name, balance)
        )

    connection.commit()
    connection.close()

def init_db():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS portfolios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            balance REAL NOT NULL DEFAULT 0
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()