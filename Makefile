.PHONY: lint format clean help

# This ensures that commands are run with the shell found by make
SHELL := /bin/bash

lint:
	@echo "✨ Running linters..."
	ruff check .
	@echo "\nRunning Pylint (on git tracked .py files)..."
	pylint $(shell git ls-files '*.py')

format:
	@echo "🎨 Formatting and auto-fixing..."
	ruff format .
	ruff check . --fix

clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf build/ dist/ *.egg-info/ .coverage htmlcov/ .tox/

help:
	@echo "Makefile for mongo_db_project"
	@echo ""
	@echo "Usage:"
	@echo "  make lint          Run ruff and pylint to check code quality."
	@echo "  make format        Format code with ruff and auto-fix issues."
	@echo "  make clean         Remove temporary files and build artifacts."
	@echo "  make help          Show this help message."

# Optional: A default goal can be set, e.g., 'make' would run 'make help'
# default: help
