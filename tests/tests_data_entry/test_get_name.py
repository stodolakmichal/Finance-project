import pytest
from main.data_entry import get_date
from unittest.mock import patch
from datetime import datetime


def test_get_date_with_default_datetime():
    with patch('builtins.input', return_value=''):
        date = get_date("Enter the date", True)
    assert date == datetime.today().strftime("%d-%m-%Y")


def test_get_date_with_correct_datetime():
    with patch('builtins.input', return_value='10-10-2024'):
        date = get_date("Enter the date", True)
    assert date == '10-10-2024'


def test_get_date_with_invalid_format():
    with patch('builtins.input', side_effect=['invalid date', '10-10-2024']):
        date = get_date("Enter the date", False)
        assert date == '10-10-2024'


def test_get_date_without_default_and_no_input():
    with patch('builtins.input', side_effect=['no input date', '10-10-2024']):
        date = get_date("Enter the date: ", allow_default=False)
        assert date == "10-10-2024"
