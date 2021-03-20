# makefile to manage repetitive commands

all: format lint test

format:
	@echo "********************"
	@echo "Formatting files..."
	@black .
	@isort .

lint:
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

# run 
# build
# deploy
# version
# push
# update?

