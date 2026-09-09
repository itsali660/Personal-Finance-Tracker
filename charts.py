import sqlite3
import matplotlib.pyplot as plt


def show_expense_chart():

    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM transactions
        WHERE type = 'Expense'
        GROUP BY category
    """)

    data = cursor.fetchall()

    connection.close()

    if not data:
        return

    categories = []
    amounts = []

    for row in data:
        categories.append(row[0])
        amounts.append(row[1])

    plt.figure(figsize=(8, 5))

    plt.bar(categories, amounts)

    plt.title("Expenses by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount ($)")

    plt.tight_layout()
    plt.show()

def show_income_expense_chart():

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

    labels = ["Income", "Expenses"]
    values = [income, expenses]

    plt.figure(figsize=(6, 5))

    plt.bar(labels, values)

    plt.title("Income vs Expenses")
    plt.ylabel("Amount ($)")

    plt.tight_layout()
    plt.show()