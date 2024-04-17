.PHONY: build publish format lint install test clean

# Build the project using Poetry
build:
	poetry build

# Publish the project to PyPI using Poetry
publish:
	poetry publish

# Format the code using Ruff
format:
	ruff format

# Perform linting checks using Ruff
lint:
	ruff check

# Install dependencies using Poetry
install:
	poetry install

# Run tests using Poetry (assuming you have a test script defined)
test:
	poetry run pytest

# Clean up build artifacts (adjust as needed for your project structure)
clean:
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info

# Default target to run when you just type `make`
all: format lint test build
