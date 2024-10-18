from main.data_entry import get_category
import pytest
from unittest.mock import patch


@pytest.mark.parametrize("input_value, expected_output", [
    ("I", "Income"),
    ("E", "Expense")
])
def test_get_category_correct_input(input_value, expected_output):
    with patch('builtins.input', return_value=input_value):
        category = get_category()
        assert category == expected_output


def test_get_category_wrong_input():
    with patch('builtins.input', side_effect=['X', 'Y', 'Z', 'I']):
        category = get_category()
        assert category == "Income"
