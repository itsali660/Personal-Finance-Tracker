from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from charts import (
    show_expense_chart,
    show_income_expense_chart
                    )
from database import (
    create_database,
    add_transaction,
    get_transactions,
    delete_transaction,
    update_transaction,
    get_totals
)


# --------------------------------------------------
# DATABASE
# --------------------------------------------------

create_database()


# --------------------------------------------------
# MAIN WINDOW
# --------------------------------------------------

window = tk.Tk()
window.title("Personal Finance Tracker")
window.geometry("950x800")


# --------------------------------------------------
# TITLE
# --------------------------------------------------

title_label = tk.Label(
    window,
    text="Personal Finance Tracker",
    font=("Arial", 24, "bold")
)

title_label.pack(pady=20)


# --------------------------------------------------
# TRANSACTION FORM
# --------------------------------------------------

form_frame = tk.Frame(window)
form_frame.pack(pady=10)


# Date
tk.Label(
    form_frame,
    text="Date:"
).grid(
    row=0,
    column=0,
    padx=10,
    pady=10
)

date_entry = tk.Entry(
    form_frame,
    width=25
)

date_entry.grid(
    row=0,
    column=1,
    padx=10,
    pady=10
)


# Type
tk.Label(
    form_frame,
    text="Type:"
).grid(
    row=1,
    column=0,
    padx=10,
    pady=10
)

type_box = ttk.Combobox(
    form_frame,
    values=["Income", "Expense"],
    width=22,
    state="readonly"
)

type_box.grid(
    row=1,
    column=1,
    padx=10,
    pady=10
)

type_box.set("Expense")


# Category
tk.Label(
    form_frame,
    text="Category:"
).grid(
    row=2,
    column=0,
    padx=10,
    pady=10
)

category_box = ttk.Combobox(
    form_frame,
    values=[
        "Food",
        "Gas",
        "Shopping",
        "Entertainment",
        "Bills",
        "Salary",
        "Other"
    ],
    width=22,
    state="readonly"
)

category_box.grid(
    row=2,
    column=1,
    padx=10,
    pady=10
)


# Amount
tk.Label(
    form_frame,
    text="Amount:"
).grid(
    row=3,
    column=0,
    padx=10,
    pady=10
)

amount_entry = tk.Entry(
    form_frame,
    width=25
)

amount_entry.grid(
    row=3,
    column=1,
    padx=10,
    pady=10
)


# Description
tk.Label(
    form_frame,
    text="Description:"
).grid(
    row=4,
    column=0,
    padx=10,
    pady=10
)

description_entry = tk.Entry(
    form_frame,
    width=25
)

description_entry.grid(
    row=4,
    column=1,
    padx=10,
    pady=10
)


# --------------------------------------------------
# TRANSACTION TABLE
# --------------------------------------------------

table_frame = tk.Frame(window)
table_frame.pack(pady=10)

columns = (
    "ID",
    "DATE",
    "TYPE",
    "CATEGORY",
    "AMOUNT",
    "DESCRIPTION"
)

transaction_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=10
)


transaction_table.heading("ID", text="ID")
transaction_table.heading("DATE", text="Date")
transaction_table.heading("TYPE", text="Type")
transaction_table.heading("CATEGORY", text="Category")
transaction_table.heading("AMOUNT", text="Amount")
transaction_table.heading("DESCRIPTION", text="Description")


transaction_table.column("ID", width=50)
transaction_table.column("DATE", width=110)
transaction_table.column("TYPE", width=100)
transaction_table.column("CATEGORY", width=120)
transaction_table.column("AMOUNT", width=100)
transaction_table.column("DESCRIPTION", width=220)

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=transaction_table.yview
)

transaction_table.configure(
    yscrollcommand=scrollbar.set
)

transaction_table.pack(
    side="left"
)

scrollbar.pack(
    side="right",
    fill="y"
)


# --------------------------------------------------
# SUMMARY SECTION
# --------------------------------------------------

summary_frame = tk.Frame(window)
summary_frame.pack(pady=15)


income_label = tk.Label(
    summary_frame,
    text="Total Income: $0.00",
    font=("Arial", 12, "bold")
)

income_label.grid(
    row=0,
    column=0,
    padx=20
)


expense_label = tk.Label(
    summary_frame,
    text="Total Expenses: $0.00",
    font=("Arial", 12, "bold")
)

expense_label.grid(
    row=0,
    column=1,
    padx=20
)


balance_label = tk.Label(
    summary_frame,
    text="Balance: $0.00",
    font=("Arial", 12, "bold")
)

balance_label.grid(
    row=0,
    column=2,
    padx=20
)


# --------------------------------------------------
# FUNCTIONS
# --------------------------------------------------

def load_transactions():

    # Clear the table first
    for row in transaction_table.get_children():
        transaction_table.delete(row)

    transactions = get_transactions()

    # Add database records to table
    for transaction in transactions:

        transaction_id = transaction[0]
        date = transaction[1]
        transaction_type = transaction[2]
        category = transaction[3]
        amount = transaction[4]
        description = transaction[5]

        transaction_table.insert(
            "",
            tk.END,
            values=(
                transaction_id,
                date,
                transaction_type,
                category,
                f"${amount:.2f}",
                description
            )
        )


def update_summary():

    income, expenses = get_totals()

    balance = income - expenses

    income_label.config(
        text=f"Total Income: ${income:.2f}"
    )

    expense_label.config(
        text=f"Total Expenses: ${expenses:.2f}"
    )

    balance_label.config(
        text=f"Balance: ${balance:.2f}"
    )


def clear_form():

    date_entry.delete(0, tk.END)
    category_box.set("")
    amount_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)

    type_box.set("Expense")


def save_transaction():

    date = date_entry.get()
    transaction_type = type_box.get()
    category = category_box.get()
    amount = amount_entry.get()
    description = description_entry.get()

    # Check required fields
    if date == "" or category == "" or amount == "":
        messagebox.showwarning(
            "Missing Information",
            "Please enter the date, category, and amount."
        )
        return

    # Validate date
    try:
        datetime.strptime(date, "%Y-%m-%d")

    except ValueError:
        messagebox.showerror(
            "Invalid Date",
            "Please enter the date as YYYY-MM-DD."
        )
        return

    # Validate amount
    try:
        amount = float(amount)

    except ValueError:
        messagebox.showerror(
            "Invalid Amount",
            "Amount must be a number."
        )
        return

    # Save transaction only after validation passes
    add_transaction(
        date,
        transaction_type,
        category,
        amount,
        description
    )

    messagebox.showinfo(
        "Success",
        "Transaction added successfully."
    )

    load_transactions()
    update_summary()
    clear_form()


def remove_transaction():

    selected_item = transaction_table.selection()

    if not selected_item:
        messagebox.showwarning(
            "No Transaction Selected",
            "Please select a transaction to delete."
        )
        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this transaction?"
    )

    if not confirm:
        return

    item = transaction_table.item(selected_item)

    transaction_id = item["values"][0]

    delete_transaction(transaction_id)

    load_transactions()
    update_summary()
    clear_form()

    messagebox.showinfo(
        "Success",
        "Transaction deleted successfully."
    )


def select_transaction(event):

    selected_item = transaction_table.selection()

    if selected_item:

        item = transaction_table.item(selected_item)

        values = item["values"]

        # Date
        date_entry.delete(0, tk.END)
        date_entry.insert(0, values[1])

        # Type
        type_box.set(values[2])

        # Category
        category_box.set(values[3])

        # Amount
        amount_entry.delete(0, tk.END)

        amount = str(values[4]).replace("$", "")

        amount_entry.insert(0, amount)

        # Description
        description_entry.delete(0, tk.END)
        description_entry.insert(0, values[5])


def edit_transaction():

    selected_item = transaction_table.selection()

    # Make sure a transaction is selected
    if not selected_item:
        messagebox.showwarning(
            "No Transaction Selected",
            "Please select a transaction to edit."
        )
        return

    # Get selected transaction ID
    item = transaction_table.item(selected_item)
    transaction_id = item["values"][0]

    # Get values from the form
    date = date_entry.get()
    transaction_type = type_box.get()
    category = category_box.get()
    amount = amount_entry.get()
    description = description_entry.get()

    # Check required fields
    if date == "" or category == "" or amount == "":
        messagebox.showwarning(
            "Missing Information",
            "Please fill in the required fields."
        )
        return

    # Validate date
    try:
        datetime.strptime(date, "%Y-%m-%d")

    except ValueError:
        messagebox.showerror(
            "Invalid Date",
            "Please enter the date as YYYY-MM-DD."
        )
        return

    # Validate amount
    try:
        amount = float(amount)

    except ValueError:
        messagebox.showerror(
            "Invalid Amount",
            "Amount must be a number."
        )
        return

    # Update transaction in the database
    update_transaction(
        transaction_id,
        date,
        transaction_type,
        category,
        amount,
        description
    )
    messagebox.showinfo(
        "Success",
        "Transaction updated successfully."
    )

    # Refresh the table and totals
    load_transactions()
    update_summary()

    # Clear the form
    clear_form()


# --------------------------------------------------
# BUTTONS
# --------------------------------------------------

button_frame = tk.Frame(window)
button_frame.pack(pady=10)


add_button = tk.Button(
    button_frame,
    text="Add Transaction",
    command=save_transaction,
    font=("Arial", 12)
)

add_button.grid(
    row=0,
    column=0,
    padx=10
)


update_button = tk.Button(
    button_frame,
    text="Update Transaction",
    command=edit_transaction,
    font=("Arial", 12)
)

update_button.grid(
    row=0,
    column=1,
    padx=10
)


delete_button = tk.Button(
    button_frame,
    text="Delete Transaction",
    command=remove_transaction,
    font=("Arial", 12)
)

delete_button.grid(
    row=0,
    column=2,
    padx=10
)

analytics_button = tk.Button(
    button_frame,
    text="View Analytics",
    command=show_expense_chart,
    font=("Arial", 12)
)

analytics_button.grid(
    row=0,
    column=3,
    padx=10
)

income_expense_button = tk.Button(
    button_frame,
    text="Income vs Expenses",
    command=show_income_expense_chart,
    font=("Arial", 12)
)
income_expense_button.grid(
    row=1,
    column=0,
    columnspan=4,
    pady=10
)

# --------------------------------------------------
# TABLE EVENT
# --------------------------------------------------

transaction_table.bind(
    "<<TreeviewSelect>>",
    select_transaction
)


# --------------------------------------------------
# INITIAL LOAD
# --------------------------------------------------

load_transactions()
update_summary()


# --------------------------------------------------
# START APPLICATION
# --------------------------------------------------

window.mainloop()