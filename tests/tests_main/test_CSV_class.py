import pandas as pd

from main import CSV
from unittest.mock import patch


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
