"""Module for handling user input for financial data entry."""

from datetime import datetime

DATE_FORMAT = "%d-%m-%Y"
CATEGORIES = {"I": "Income", "E": "Expense"}


def get_date(prompt: str, allow_default: bool = False) -> str:
    """Prompt the user for a date in dd-mm-yyyy format.

    Args:
        prompt: The message displayed to the user.
        allow_default: If True, an empty input returns today's date.

    Returns:
        A validated date string in dd-mm-yyyy format.
    """
    while True:
        date_str = input(prompt)
        if allow_default and not date_str:
            return datetime.today().strftime(DATE_FORMAT)

        try:
            valid_date = datetime.strptime(date_str, DATE_FORMAT)
            return valid_date.strftime(DATE_FORMAT)
        except ValueError:
            print("Invalid date format. Please enter the date in dd-mm-yyyy format")


def get_amount() -> float:
    """Prompt the user for a positive monetary amount.

    Returns:
        A positive float representing the transaction amount.
    """
    while True:
        try:
            amount = float(input("Enter the amount: "))
            if amount <= 0:
                raise ValueError("Amount must be a non-negative non-zero value.")
            return amount
        except ValueError as e:
            print(e)


def get_category() -> str:
    """Prompt the user to select a transaction category.

    Returns:
        A string, either 'Income' or 'Expense'.
    """
    while True:
        category = input("Enter the category ('I' for Income or 'E' for Expense): ").upper()
        if category in CATEGORIES:
            return CATEGORIES[category]
        print("Invalid category. Please enter 'I' for Income or 'E' for Expense.")


def get_description() -> str:
    """Prompt the user for an optional transaction description.

    Returns:
        A string with the description (may be empty).
    """
    return input("Enter a description (optional): ")
