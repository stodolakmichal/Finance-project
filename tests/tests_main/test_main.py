from main import main
from unittest.mock import patch


def test_main_option_1():
    with patch("builtins.input", side_effect=['1', '3']):
        with patch("main.add") as mocked_add:
            main()
            mocked_add.assert_called_once()


def test_main_option_2_without_plot():
    with patch("builtins.input", side_effect=['2', 'n', '3']):
        with patch("main.get_date", side_effect=['01-01-2000', '01-01-2222']):
            with patch("main.CSV.get_transactions") as mocked_get_transactions:
                main()
                mocked_get_transactions.assert_called_once_with('01-01-2000', '01-01-2222')


def test_main_option_2_with_plot():
    with patch("builtins.input", side_effect=['2', 'y', '3']):
        with patch("main.get_date", side_effect=['01-01-2000', '01-01-2222']):
            with patch("main.CSV.get_transactions") as mocked_get_transactions:
                with patch("main.plot_transaction") as mocked_plot_transaction:
                    main()
                    mocked_get_transactions.assert_called_once_with('01-01-2000', '01-01-2222')
                    mocked_plot_transaction.assert_called_once()


def test_main_option_3():
    with patch("builtins.input", side_effect=['3']):
        with patch("builtins.print") as mocked_print:
            main()
            mocked_print.assert_any_call("Exiting...")


def test_main_invalid_option():
    with patch("builtins.input", side_effect=['Invalid option', '3']):
        with patch("builtins.print") as mocked_print:
            main()
            mocked_print.assert_any_call("Invalid choice. Enter 1, 2, or 3.")
