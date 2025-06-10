.PHONY: help
help:
	@echo "Usage: make <target>"
	@echo "Targets:"
	@echo "  clean-cache - Clean cache files"

.PHONY: clean-cache
clean-cache:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".ruff_cache" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type f -name ".coverage" -delete
