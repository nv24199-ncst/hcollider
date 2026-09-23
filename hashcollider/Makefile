.PHONY: install test lint format run clean

install:
	python3 -m pip install -e ".[dev]"

test:
	pytest -v

lint:
	python3 -m py_compile $$(find src -name "*.py")

format:
	python3 -m pip show black > /dev/null 2>&1 && black src tests || echo "black not installed; skipping"

run:
	python3 -m hashcollider algorithms

clean:
	rm -rf build dist *.egg-info .pytest_cache .coverage htmlcov
	find . -type d -name "__pycache__" -exec rm -rf {} +
