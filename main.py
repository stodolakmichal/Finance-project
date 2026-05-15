"""Personal finance tracker CLI application.

Allows users to add transactions, view summaries, and plot income vs expenses.
"""

from __future__ import annotations

import csv
from datetime import datetime
from typing import List

import matplotlib.pyplot as plt
import pandas as pd

from functions.data_entry import get_category, get_amount, get_date, get_description

DEFAULT_CSV_FILE = "finance_data.csv"


class CSV:
    """Manages reading and writing financial transaction data to a CSV file.

    Attributes:
        csv_file: Path to the CSV file used for storage.
        COLUMNS: Column names for the CSV file.
        FORMAT: Date format string used throughout the application.
    """

    COLUMNS: list[str] = ["date", "amount", "category", "description"]
    FORMAT: str = "%d-%m-%Y"

    def __init__(self, csv_file: str = DEFAULT_CSV_FILE) -> None:
        """Initialize the CSV manager with a file path.

        Args:
            csv_file: Path to the CSV file. Defaults to 'finance_data.csv'.
        """
        self.csv_file = csv_file

    def initialize_csv(self) -> None:
        """Create the CSV file with headers if it does not already exist."""
        try:
            pd.read_csv(self.csv_file)
        except FileNotFoundError:
            df = pd.DataFrame(columns=self.COLUMNS)
            df.to_csv(self.csv_file, index=False)

    def add_entry(self, date: str, amount: float, category: str, description: str) -> None:
        """Append a new transaction entry to the CSV file.

        Args:
            date: Transaction date in dd-mm-yyyy format.
            amount: Transaction amount (positive float).
            category: Either 'Income' or 'Expense'.
            description: Optional description of the transaction.
        """
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
        }
        with open(self.csv_file, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully!")

    def get_transactions(self, start_date: str, end_date: str) -> pd.DataFrame:
        """Retrieve and display transactions within a date range.

        Args:
            start_date: Start date in dd-mm-yyyy format.
            end_date: End date in dd-mm-yyyy format.

        Returns:
            A filtered DataFrame with transactions in the given range.
            Returns an empty DataFrame if an error occurs.
        """
        try:
            df = pd.read_csv(self.csv_file)
        except FileNotFoundError:
            print(f"Error: File '{self.csv_file}' not found. Please add a transaction first.")
            return pd.DataFrame(columns=self.COLUMNS)
        except pd.errors.EmptyDataError:
            print(f"Error: File '{self.csv_file}' is empty.")
            return pd.DataFrame(columns=self.COLUMNS)
        except pd.errors.ParserError:
            print(f"Error: File '{self.csv_file}' is corrupted or has invalid format.")
            return pd.DataFrame(columns=self.COLUMNS)

        df["date"] = pd.to_datetime(df["date"].str.strip(), format=self.FORMAT)
        df = df.sort_values(by="date")
        start = datetime.strptime(start_date, self.FORMAT)
        end = datetime.strptime(end_date, self.FORMAT)

        mask = (df["date"] >= start) & (df["date"] <= end)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found in the given date range")
        else:
            print(
                f"Transactions from {start.strftime(self.FORMAT)} to {end.strftime(self.FORMAT)}"
            )
            print(
                filtered_df.to_string(
                    index=False, formatters={"date": lambda x: x.strftime(self.FORMAT)}
                )
            )

            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            print("\nSummary: ")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${total_income - total_expense:.2f}")

        return filtered_df


def add(csv_manager: CSV) -> None:
    """Guide the user through adding a new transaction.

    Args:
        csv_manager: The CSV instance to store data in.
    """
    csv_manager.initialize_csv()
    date = get_date(
        "Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ",
        allow_default=True,
    )
    amount = get_amount()
    category = get_category()
    description = get_description()
    csv_manager.add_entry(date, amount, category, description)


def plot_transaction(df: pd.DataFrame) -> None:
    """Plot income and expenses over time from a DataFrame.

    Creates a line chart showing daily income and expenses.
    Does not modify the original DataFrame.

    Args:
        df: A DataFrame with 'date', 'category', and 'amount' columns.
    """
    if df.empty:
        print("No data to plot.")
        return

    plot_df = df.copy()
    plot_df = plot_df.set_index("date")

    income_df = (
        plot_df[plot_df["category"] == "Income"]
        .resample("D")
        .sum(numeric_only=True)
        .reindex(plot_df.index, fill_value=0)
    )
    expense_df = (
        plot_df[plot_df["category"] == "Expense"]
        .resample("D")
        .sum(numeric_only=True)
        .reindex(plot_df.index, fill_value=0)
    )

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()


def main() -> None:
    """Run the main interactive loop of the finance tracker."""
    csv_manager = CSV()

    while True:
        print("1. Add a new transaction")
        print("2. View transactions and a summary with a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add(csv_manager)
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = csv_manager.get_transactions(start_date, end_date)
            if not df.empty and input("Do you want to see a plot? (y/n) ").lower() == "y":
                plot_transaction(df)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
