# makefile to manage repetitive commands

all: format lint test

format:
	@echo "********************"
	@echo "Formatting files..."
	@black . --target-version py38
	@isort .

lint:
	@echo "********************"
	@echo "Type checking files..."
	@mypy .
	@echo "********************"
	@echo "Linting files..."
	@flake8 --docstring-convention google

test:
	@echo "********************"
	@echo "Testing..."
	@pytest --color=yes

test-cov:
	@echo "********************"
	@echo "Testing with Coverage..."
	@pytest --cov

run:
	@poetry run initialize

