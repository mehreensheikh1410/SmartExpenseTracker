import sqlite3
import matplotlib.pyplot as plt

# Connect to database
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

# Create expenses table
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    category TEXT,
    description TEXT
)
""")

conn.commit()

# Ask for monthly budget
budget = float(input("Enter your monthly budget: ₹"))

while True:

    print("\n===== SMART EXPENSE TRACKER =====")
    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. Total Spending")
    print("4. Budget Remaining")
    print("5. Category Spending")
    print("6. Spending Graph")
    print("7. Delete Expense")
    print("8. Exit")

    choice = input("Enter your choice: ")

    # Add Expense
    if choice == "1":

        amount = float(input("Enter amount: ₹"))
        category = input("Enter category: ")
        description = input("Enter description: ")

        cursor.execute(
            "INSERT INTO expenses (amount, category, description) VALUES (?, ?, ?)",
            (amount, category, description)
        )

        conn.commit()

        print("Expense added successfully!")

    # View All Expenses
    elif choice == "2":

        cursor.execute("SELECT * FROM expenses")
        expenses = cursor.fetchall()

        if not expenses:
            print("No expenses found.")

        else:
            print("\nID | Amount | Category | Description")
            print("--------------------------------------")

            for expense in expenses:
                print(expense)

    # Total Spending
    elif choice == "3":

        cursor.execute("SELECT SUM(amount) FROM expenses")
        total = cursor.fetchone()[0] or 0

        print("Total Spending: ₹", round(total, 2))

    # Budget Remaining
    elif choice == "4":

        cursor.execute("SELECT SUM(amount) FROM expenses")
        total = cursor.fetchone()[0] or 0

        remaining = budget - total

        print("Monthly Budget: ₹", round(budget, 2))
        print("Total Spending: ₹", round(total, 2))
        print("Budget Remaining: ₹", round(remaining, 2))

        if remaining < 0:
            print("Warning: You have exceeded your budget!")

    # Category Spending
    elif choice == "5":

        cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
        """)

        categories = cursor.fetchall()

        if not categories:
            print("No expenses found.")

        else:
            print("\nCategory Spending:")

            for category, amount in categories:
                print(category, ": ₹", round(amount, 2))

    # Spending Graph
    elif choice == "6":

        cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
        """)

        data = cursor.fetchall()

        if not data:
            print("No expenses available for graph.")

        else:
            categories = [row[0] for row in data]
            amounts = [row[1] for row in data]

            plt.bar(categories, amounts)
            plt.xlabel("Category")
            plt.ylabel("Amount Spent")
            plt.title("Spending by Category")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

    # Delete Expense
    elif choice == "7":

        cursor.execute("SELECT * FROM expenses")
        expenses = cursor.fetchall()

        if not expenses:
            print("No expenses to delete.")

        else:
            print("\nYour Expenses:")

            for expense in expenses:
                print(expense)

            expense_id = int(input("Enter Expense ID to delete: "))

            cursor.execute(
                "DELETE FROM expenses WHERE id = ?",
                (expense_id,)
            )

            conn.commit()

            if cursor.rowcount > 0:
                print("Expense deleted successfully!")

            else:
                print("Expense ID not found.")

    # Exit
    elif choice == "8":

        print("Thank you for using Smart Expense Tracker!")
        break

    # Invalid Choice
    else:

        print("Invalid choice. Please try again.")

# Close database
conn.close()