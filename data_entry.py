# data_entry.py

from datetime import datetime

DATE_FORMAT = "%d-%m-%Y"
CATEGORIES = {"I": "Income", "E": "Expense"}


def get_date(prompt, allow_default=False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(DATE_FORMAT)

    try:
        valid_date = datetime.strptime(date_str, DATE_FORMAT)
        return valid_date.strftime(DATE_FORMAT)
    except ValueError:
        print("❌ Invalid date. Please use dd-mm-yyyy format.")
        return get_date(prompt, allow_default)


def get_amount():
    try:
        amount = float(input("💰 Enter amount: "))
        if amount <= 0:
            raise ValueError("Amount must be a positive number.")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()


def get_category():
    category = input("📂 Category? ('I' for Income, 'E' for Expense): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]
    print("❌ Invalid category. Please enter 'I' or 'E'.")
    return get_category()


def get_description():
    return input("📝 Description (optional): ")
