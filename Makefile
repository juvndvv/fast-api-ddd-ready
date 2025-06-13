.PHONY: help
help:
	@echo "Usage: make <target>"
	@echo "Targets:"
	@echo "  start       - Start the application"
	@echo "  stop        - Stop the application"
	@echo "  test        - Run all tests with pytest"
	@echo "  test-unit   - Run only unit tests"
	@echo "  test-integration - Run only integration tests"
	@echo "  test-e2e    - Run only end-to-end tests"
	@echo "  quality     - Run code quality checks (ruff + mypy)"
	@echo "  install     - Install dependencies"
	@echo "  clean-cache - Clean cache files"

.PHONY: install
install:
	uv sync --dev

.PHONY: start
start:
	@echo "Starting the application..."
	docker compose up

.PHONY: stop
stop:
	@echo "Stopping the application..."
	@pkill -f "python main.py" || echo "No running processes found"

.PHONY: test
test:
	@echo "Running all tests..."
	uv run pytest

.PHONY: test-unit
test-unit:
	@echo "Running unit tests..."
	uv run pytest -m unit

.PHONY: test-integration
test-integration:
	@echo "Running integration tests..."
	uv run pytest -m integration

.PHONY: test-e2e
test-e2e:
	@echo "Running end-to-end tests..."
	uv run pytest -m e2e

.PHONY: quality
quality:
	@echo "Running code quality checks..."
	@echo "Running ruff..."
	uv run ruff check app tests
	@echo "Running mypy..."
	uv run mypy app

.PHONY: clean-cache
clean-cache:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".ruff_cache" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type f -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -r {} +
