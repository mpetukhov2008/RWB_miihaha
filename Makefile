.PHONY: install test lint run-case1 clean

PYTHON ?= python3
PIP ?= pip3

install:
	$(PYTHON) -m pip install -e ".[dev]"

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m ruff check .
	$(PYTHON) -m mypy pipeline

run-case1:
	LLM_MODE=mock $(PYTHON) -m pipeline.main run --requirements examples/case1.md

clean:
	rm -rf runs/ .pytest_cache/ .mypy_cache/ .ruff_cache/
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete