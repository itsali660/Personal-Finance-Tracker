import sqlite3

def create_database():
    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        type TEXT NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        description TEXT
    )
    """)
    connection.commit()
    connection.close()

def add_transaction(date, transaction_type, category, amount, description):
    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO transactions (date, type, category, amount, description)
    VALUES (?, ?, ?, ?, ?)
    """, (date, transaction_type, category, amount, description))
    connection.commit()
    connection.close()

def get_transactions():
    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM transactions")
    transactions = cursor.fetchall()
    connection.close()
    return transactions

def delete_transaction(transaction_id):
    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()
    cursor.execute(
        "DELETE FROM transactions WHERE id = ?",
        (transaction_id,)
    )
    connection.commit()
    connection.close()

def update_transaction(
        transaction_id,
        date,
        transaction_type,
        category,
        amount,
        description
):
    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE transactions
        SET date = ?,
            type = ?,
            category = ?,
            amount = ?,
            description = ?
        WHERE id = ?
    """, (
        date,
        transaction_type,
        category,
        amount,
        description,
        transaction_id
    ))

    connection.commit()
    connection.close()

def get_totals():

    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()
    cursor.execute("""
        SELECT SUM(amount)
        FROM transactions
        WHERE type = 'Income'
    """)
    income = cursor.fetchone()[0]
    cursor.execute("""
        SELECT SUM(amount)
        FROM transactions
        WHERE type = 'Expense'
    """)

    expenses = cursor.fetchone()[0]
    connection.close()

    if income is None:
        income = 0
    if expenses is None:
        expenses = 0
    return income, expenses