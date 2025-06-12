# main.py

import pandas as pd
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt
from data_entry import get_date, get_amount, get_category, get_description

class Transaction:
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
            "description": self.description,
        }

class DataManager:   
    FILE_NAME = os.path.join(os.path.dirname(__file__), "finance_data.csv")
    COLUMNS = ["date", "amount", "category", "description"]
    DATE_FORMAT = "%d-%m-%Y"

    def __init__(self):
        self._initialize_csv()

    def _initialize_csv(self):
        if not os.path.exists(self.FILE_NAME):
            df = pd.DataFrame(columns=self.COLUMNS)
            df.to_csv(self.FILE_NAME, index=False)

    def add_transaction(self, transaction: Transaction):
        with open(self.FILE_NAME, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.COLUMNS)
            writer.writerow(transaction.to_dict())
        print("✅ Transaction added successfully!")

    def get_transactions(self, start_date, end_date):
        try:
            df = pd.read_csv(self.FILE_NAME)
            df["date"] = pd.to_datetime(df["date"], format=self.DATE_FORMAT, errors='coerce')
            df = df.dropna(subset=["date"])  # Drop bad rows

            start = datetime.strptime(start_date, self.DATE_FORMAT)
            end = datetime.strptime(end_date, self.DATE_FORMAT)

            mask = (df["date"] >= start) & (df["date"] <= end)
            filtered = df.loc[mask]

            if filtered.empty:
                print("⚠️ No transactions found in the given date range.")
                return pd.DataFrame()
            else:
                print(f"\n🧾 Transactions from {start_date} to {end_date}:\n")
                print(filtered.to_string(index=False, formatters={"date": lambda x: x.strftime(self.DATE_FORMAT)}))

                income = filtered[filtered["category"] == "Income"]["amount"].sum()
                expense = filtered[filtered["category"] == "Expense"]["amount"].sum()

                print("\n📊 Summary:")
                print(f"Total Income: ₹{income:.2f}")
                print(f"Total Expense: ₹{expense:.2f}")
                print(f"Net Savings: ₹{(income - expense):.2f}")

                return filtered
        except Exception as e:
            print(f"❌ Error reading CSV: {e}")
            return pd.DataFrame()


class ExpenseTracker:
    def __init__(self):
        self.manager = DataManager()

    def add_transaction(self):
        date = get_date("📅 Enter date (dd-mm-yyyy) or press Enter for today: ", allow_default=True)
        amount = get_amount()
        category = get_category()
        description = get_description()
        txn = Transaction(date, amount, category, description)
        self.manager.add_transaction(txn)

    def view_summary_and_plot(self):
        start_date = get_date("📅 Enter start date (dd-mm-yyyy): ")
        end_date = get_date("📅 Enter end date (dd-mm-yyyy): ")
        df = self.manager.get_transactions(start_date, end_date)

        if not df.empty:
            plot_choice = input("\n📈 Show graph? (y/n): ").strip().lower()
            if plot_choice == 'y':
                self.plot(df)

    def plot(self, df):
        df.set_index("date", inplace=True)

        income_df = df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0)
        expense_df = df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0)

        plt.figure(figsize=(10, 5))
        plt.plot(income_df.index, income_df["amount"], label="Income", color="green", marker='o')
        plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="red", marker='x')
        plt.title("📊 Income vs Expense Over Time")
        plt.xlabel("Date")
        plt.ylabel("Amount (₹)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()


def main():
    tracker = ExpenseTracker()

    while True:
        print("\n========= Personal Expense Manager =========")
        print("1. ➕ Add New Transaction")
        print("2. 📂 View Transactions & Summary")
        print("3. ❌ Exit")
        choice = input("👉 Enter your choice (1-3): ")

        if choice == "1":
            tracker.add_transaction()
        elif choice == "2":
            tracker.view_summary_and_plot()
        elif choice == "3":
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("⚠️ Invalid input. Please enter 1, 2 or 3.")


if __name__ == "__main__":
    main()
