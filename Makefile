.PHONY: help install lint format test test-cov run analyze clean

## help: Show available commands
help:
	@echo "E-Commerce Trend Analysis — Available commands:"
	@sed -n 's/^##//p' $(MAKEFILE_LIST) | column -t -s ':' | sed -e 's/^/ /'

## install: Install dependencies
install:
	pip install -r requirements.txt
	pre-commit install

## lint: Run flake8
lint:
	flake8 src/ tests/ --max-line-length=120 --ignore=E203,W503

## format: Format with Black + isort
format:
	black src/ tests/ --line-length 120
	isort src/ tests/

## test: Run tests
test:
	pytest tests/ -v --tb=short

## test-cov: Run tests with coverage
test-cov:
	pytest tests/ -v --cov=src --cov-report=term-missing

## run: Fetch API data and run full analysis
run:
	python -m src.main

## analyze: Run market basket analysis only
analyze:
	python -m src.analysis --input data/processed/transactions.csv

## clean: Remove cache and artifacts
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	rm -rf .pytest_cache htmlcov .coverage
