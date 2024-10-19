import pandas as pd

from main import CSV
from unittest.mock import patch, mock_open
from io import StringIO


class TestCSV:
    def test_initialize_csv_file_exists(self):
        with patch('pandas.read_csv') as mock_read_csv:
            CSV.initialize_csv()
            mock_read_csv.assert_called_once_with(CSV.CSV_FILE)

    def test_initialize_csv_file_not_found(self):
        with patch('pandas.read_csv', side_effect=FileNotFoundError):
            with patch('pandas.DataFrame.to_csv') as mock_to_csv:
                CSV.initialize_csv()
                df = pd.DataFrame(columns=CSV.COLUMNS)
                mock_to_csv.assert_called_once_with(CSV.CSV_FILE, index=False)
                assert list(df.columns) == CSV.COLUMNS

    def test_add_entry(self):
        entry = {
            "date": "01-01-2020",
            "amount": "350",
            "category": "Test_category",
            "description": "Test_description"
        }
        with patch('builtins.open', mock_open()) as mock_file:
            with patch('csv.DictWriter') as mock_DictWriter:
                mock_writer_instance = mock_DictWriter.return_value
                CSV.add_entry(**entry)
                mock_file.assert_called_once_with(CSV.CSV_FILE, "a", newline="")
                mock_DictWriter.assert_called_once_with(mock_file(), fieldnames=CSV.COLUMNS)
                mock_writer_instance.writerow.assert_called_once_with(entry)

    def test_get_transactions(self):
        csv_data = """date,amount,category,description
    01-10-2024,1000,Income,Salary
    02-10-2024,500,Expense,Rent
    03-10-2024,200,Income,Freelance
    05-10-2024,150,Expense,Groceries
    07-10-2024,300,Income,Bonus
    """

        with patch("pandas.read_csv", return_value=pd.read_csv(StringIO(csv_data))):
            result = CSV.get_transactions("01-10-2024", "05-10-2024")

            assert len(result) == 4
            assert result["amount"].sum() == 1850

            total_income = result[result["category"] == "Income"]["amount"].sum()
            total_expense = result[result["category"] == "Expense"]["amount"].sum()

            assert total_income == 1200
            assert total_expense == 650
            assert (total_income - total_expense) == 550
