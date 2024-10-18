import pytest
from main.data_entry import get_amount
from unittest.mock import patch
from datetime import datetime


def test_get_amount_zero():
    with patch('builtins.input', side_effect=['0', '1']):
        amount = get_amount()
        assert amount == 1


def test_get_amount_negative_value():
    with patch('builtins.input', side_effect=['-100', '-200', '100']):
        amount = get_amount()
        assert amount == 100


def test_get_amount_wrong_value():
    with patch('builtins.input', side_effect=['a', 'b', '100']):
        amount = get_amount()
        assert amount == 100


@pytest.mark.parametrize("input_value, expected_output", [
    ("100", 100.0),
    ("250.5", 250.5),
    ("1", 1),
    ("0.00000001", 0.00000001)
])
def test_get_amount_correct_value(input_value, expected_output):
    with patch('builtins.input', return_value=input_value):
        amount = get_amount()
        assert amount == expected_output
