from main.data_entry import get_description
from unittest.mock import patch


def test_get_description():
    with patch('builtins.input', return_value="Example description"):
        description = get_description()
        assert description == "Example description"
