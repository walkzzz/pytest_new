# Pytest New

A pytest-based automation testing framework with pywinauto and Allure reporting.

## Features

- **Pytest Framework**: Python testing framework
- **Pywinauto**: Windows UI automation testing
- **Allure Reports**: Beautiful test reports
- **YAML Configuration**: Easy-to-use test case configuration

## Requirements

- Python 3.10+
- Windows OS

## Installation

```bash
pip install -r requirements.txt
```

## Running Tests

```powershell
# Run all tests
python -m pytest tests --alluredir=allure-results

# Or use the PowerShell script
.\run_test.ps1
```

## Generate Allure Report

```bash
allure generate allure-results -o allure-report
allure open allure-report
```

## Project Structure

```
pytest_new/
├── src/
│   ├── allure/           # Allure helpers
│   ├── config/           # Configuration parsing
│   ├── pytest_runner/    # Test runner
│   └── pywinauto/        # UI automation
├── tests/
│   ├── configs/          # Test configurations (YAML)
│   └── test_*.py         # Test cases
├── requirements.txt     # Python dependencies
└── run_test.ps1         # Run script
```

## Configuration

Test cases are defined in YAML files under `tests/configs/`.
