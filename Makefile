.PHONY: help lint test typecheck coverage clean install install-dev

help:
	@echo "Available commands:"
	@echo "  install       Install production dependencies"
	@echo "  install-dev   Install development dependencies"
	@echo "  lint          Run code style checks (black, isort, flake8)"
	@echo "  test          Run all tests"
	@echo "  test-unit     Run unit tests only"
	@echo "  test-example  Run example tests only"
	@echo "  typecheck     Run mypy type checking"
	@echo "  coverage      Generate test coverage report"
	@echo "  clean         Clean generated files"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

lint:
	black --check .
	isort --check-only .
	flake8 .

lint-fix:
	black .
	isort .

test:
	pytest -v --tb=short

test-unit:
	pytest tests/unit/ -v --tb=short

test-example:
	pytest tests/example/ -v --tb=short --ignore=tests/example/test_parametrization_advanced.py

typecheck:
	mypy src/

coverage:
	pytest --cov=src --cov-report=html --cov-report=xml

clean:
	rm -rf .pytest_cache .coverage htmlcov coverage.xml
	rm -rf reports screenshots logs data
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".DS_Store" -delete