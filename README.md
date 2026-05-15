# Finance Project

A personal finance tracker CLI application for managing income and expenses.

## Features

- **Add transactions** — record income and expenses with date, amount, category, and description.
- **View transactions** — filter and display transactions within a date range with a summary.
- **Plot data** — visualize income vs expenses over time using matplotlib.

## Installation

```bash
# Clone the repository
git clone https://github.com/stodolakmichal/Finance-project.git
cd Finance-project

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -e .

# Install dev dependencies (for testing & linting)
pip install -e ".[dev]"
```

## Usage

```bash
python main.py
```

You will see an interactive menu:

```
1. Add a new transaction
2. View transactions and a summary with a date range
3. Exit
```

## Data Storage

Transactions are stored in `finance_data.csv`. A sample file is provided as `finance_data.example.csv`.

To start fresh, copy the example file:

```bash
cp finance_data.example.csv finance_data.csv
```

## Running Tests

```bash
pytest
```

## Project Structure

```
Finance-project/
├── main.py                  # Main application logic and CSV class
├── functions/
│   ├── __init__.py
│   └── data_entry.py        # User input functions with validation
├── tests/
│   ├── tests_data_entry/    # Unit tests for input functions
│   └── tests_main/          # Unit tests for CSV class and main flow
├── finance_data.example.csv # Example data file
├── pyproject.toml           # Project metadata and dependencies
├── .flake8                  # Flake8 configuration
├── .pre-commit-config.yaml  # Pre-commit hooks configuration
└── .gitignore
```

## Development

This project uses:

- **flake8** for linting
- **pytest** for testing
- **pre-commit** hooks for code quality checks

Install pre-commit hooks:

```bash
pre-commit install
```
