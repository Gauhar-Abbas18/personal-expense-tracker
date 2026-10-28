"""
Personal Expense Tracker
Beginner Python project for learning lists, dictionaries, functions, loops,
input validation, and saving data to a JSON file.
"""

import json
from pathlib import Path
from datetime import date

DATA_FILE = Path("expenses.json")


def load_transactions():
    """Load saved transactions, or start with an empty list."""
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        print("Could not read saved data. Starting with an empty list.")
        return []


def save_transactions(transactions):
    """Save transactions locally as JSON."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(transactions, file, indent=2, ensure_ascii=False)


def read_amount():
    """Ask for a positive amount and validate the input."""
    while True:
        raw_value = input("Amount: ").strip()
        try:
            amount = float(raw_value)
            if amount <= 0:
                print("Enter an amount greater than zero.")
                continue
            return round(amount, 2)
        except ValueError:
            print("Please enter a valid number, for example 12.50.")


def add_transaction(transactions):
    """Create and save one income or expense record."""
    print("\nAdd transaction")
    kind = input("Type (income/expense): ").strip().lower()
    while kind not in ("income", "expense"):
        print("Please type 'income' or 'expense'.")
        kind = input("Type (income/expense): ").strip().lower()

    description = input("Description: ").strip()
    while not description:
        print("Description cannot be empty.")
        description = input("Description: ").strip()

    category = input("Category (food/transport/study/housing/salary/other): ").strip()
    if not category:
        category = "other"

    transaction_date = input(f"Date (YYYY-MM-DD, Enter for {date.today()}): ").strip()
    if not transaction_date:
        transaction_date = date.today().isoformat()
    else:
        try:
            date.fromisoformat(transaction_date)
        except ValueError:
            print("Invalid date; using today's date.")
            transaction_date = date.today().isoformat()

    amount = read_amount()
    transactions.append({
        "type": kind,
        "description": description,
        "category": category,
        "date": transaction_date,
        "amount": amount,
    })
    save_transactions(transactions)
    print("Transaction saved.")


def show_summary(transactions):
    """Display total income, expenses, and remaining balance."""
    income = sum(item["amount"] for item in transactions if item["type"] == "income")
    expenses = sum(item["amount"] for item in transactions if item["type"] == "expense")
    print("\n--- Summary ---")
    print(f"Total income:   {income:.2f}")
    print(f"Total expenses: {expenses:.2f}")
    print(f"Balance:        {income - expenses:.2f}")
    print(f"Transactions:   {len(transactions)}")


def list_transactions(transactions):
    """Print all saved transactions."""
    print("\n--- Transactions ---")
    if not transactions:
        print("No transactions yet.")
        return

    for number, item in enumerate(transactions, start=1):
        sign = "+" if item["type"] == "income" else "-"
        print(
            f"{number}. {item['date']} | {item['description']} | "
            f"{item['category']} | {item['type']} | "
            f"{sign}{item['amount']:.2f}"
        )


def delete_transaction(transactions):
    """Delete a transaction selected by its number."""
    list_transactions(transactions)
    if not transactions:
        return

    try:
        number = int(input("Enter transaction number to delete: "))
        if not 1 <= number <= len(transactions):
            print("That number is not in the list.")
            return
    except ValueError:
        print("Please enter a whole number.")
        return

    removed = transactions.pop(number - 1)
    save_transactions(transactions)
    print(f"Deleted: {removed['description']}")


def main():
    transactions = load_transactions()

    while True:
        print("\n=== PERSONAL EXPENSE TRACKER ===")
        print("1. Add transaction")
        print("2. View summary")
        print("3. List transactions")
        print("4. Delete transaction")
        print("5. Exit")

        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            add_transaction(transactions)
        elif choice == "2":
            show_summary(transactions)
        elif choice == "3":
            list_transactions(transactions)
        elif choice == "4":
            delete_transaction(transactions)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Please choose a number from 1 to 5.")


if __name__ == "__main__":
    main()
