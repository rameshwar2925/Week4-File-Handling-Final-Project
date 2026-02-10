import json
import csv
import os
from datetime import datetime
from collections import defaultdict

DATA_FILE = "expenses.json"
BACKUP_FILE = "expenses_backup.json"
EXPORT_FILE = "expenses_export.csv"
CATEGORIES = ["Food", "Transport", "Entertainment", "Bills", "Shopping", "Other"]


class Expense:
    def __init__(self, date, amount, category, description):
        self.date = date
        self.amount = amount
        self.category = category
        self.description = description

    def to_dict(self):
        return {
            "date": self.date,
            "amount": self.amount,
            "category": self.category,
            "description": self.description
        }


class FinanceTracker:
    def __init__(self):
        self.expenses = []
        self.load_data()

    # ---------- FILE HANDLING ----------
    def load_data(self):
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r") as file:
                    data = json.load(file)
                    self.expenses = [Expense(**e) for e in data]
        except Exception as e:
            print("Error loading data:", e)

    def save_data(self):
        try:
            self.backup_data()
            with open(DATA_FILE, "w") as file:
                json.dump([e.to_dict() for e in self.expenses], file, indent=4)
        except Exception as e:
            print("Error saving data:", e)

    def backup_data(self):
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r") as src, open(BACKUP_FILE, "w") as dst:
                    dst.write(src.read())
        except Exception as e:
            print("Backup failed:", e)

    # ---------- CORE FEATURES ----------
    def add_expense(self):
        try:
            date = input("Date (YYYY-MM-DD): ").strip()
            datetime.strptime(date, "%Y-%m-%d")

            amount = float(input("Amount: "))
            if amount <= 0:
                raise ValueError

            print("Categories:", ", ".join(CATEGORIES))
            category = input("Category: ").strip()
            if category not in CATEGORIES:
                category = "Other"

            description = input("Description: ").strip()

            self.expenses.append(Expense(date, amount, category, description))
            self.save_data()
            print("Expense added successfully!")

        except ValueError:
            print("Invalid input! Expense not added.")

    def view_expenses(self):
        if not self.expenses:
            print("No expenses found.")
            return

        print("\nDate        Amount   Category        Description")
        print("-" * 55)
        for e in self.expenses:
            print(f"{e.date}  {e.amount:7.2f}  {e.category:<14} {e.description}")

    def search_expenses(self):
        keyword = input("Search keyword: ").lower()
        results = [e for e in self.expenses if keyword in e.description.lower()]

        if not results:
            print("No matching expenses.")
            return

        for e in results:
            print(e.date, e.amount, e.category, e.description)

    # ---------- REPORTS ----------
    def monthly_report(self):
        month = input("Enter month (YYYY-MM): ")
        total = 0
        for e in self.expenses:
            if e.date.startswith(month):
                total += e.amount
        print(f"Total expenses for {month}: ₹{total:.2f}")

    def category_report(self):
        summary = defaultdict(float)
        for e in self.expenses:
            summary[e.category] += e.amount

        print("\nCategory-wise Breakdown")
        print("-" * 30)
        for cat, amt in summary.items():
            print(f"{cat:<15}: ₹{amt:.2f}")

    def statistics(self):
        if not self.expenses:
            print("No data available.")
            return

        amounts = [e.amount for e in self.expenses]
        print("Total Expenses :", sum(amounts))
        print("Highest Expense:", max(amounts))
        print("Lowest Expense :", min(amounts))
        print("Average Expense:", sum(amounts) / len(amounts))

    # ---------- EXPORT ----------
    def export_csv(self):
        try:
            with open(EXPORT_FILE, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Amount", "Category", "Description"])
                for e in self.expenses:
                    writer.writerow([e.date, e.amount, e.category, e.description])
            print("Data exported to CSV successfully!")
        except Exception as e:
            print("Export failed:", e)

    # ---------- MENU ----------
    def run(self):
        while True:
            print("\n" + "=" * 50)
            print("        PERSONAL FINANCE TRACKER")
            print("=" * 50)
            print("1. Add Expense")
            print("2. View Expenses")
            print("3. Search Expenses")
            print("4. Monthly Report")
            print("5. Category Report")
            print("6. View Statistics")
            print("7. Export to CSV")
            print("0. Exit")

            choice = input("Enter choice: ").strip()

            if choice == "1":
                self.add_expense()
            elif choice == "2":
                self.view_expenses()
            elif choice == "3":
                self.search_expenses()
            elif choice == "4":
                self.monthly_report()
            elif choice == "5":
                self.category_report()
            elif choice == "6":
                self.statistics()
            elif choice == "7":
                self.export_csv()
            elif choice == "0":
                print("Thank you for using Finance Tracker!")
                break
            else:
                print("Invalid choice!")


if __name__ == "__main__":
    FinanceTracker().run()
