.PHONY: test test-unit test-integration test-e2e lint format setup

setup:
	uv sync

test:
	uv run pytest tests/ -v --tb=short

test-unit:
	uv run pytest tests/ -v --tb=short -m "not integration and not e2e"

test-integration:
	uv run pytest tests/ -v --tb=short -m integration

test-e2e:
	uv run pytest tests/ -v --tb=short -m e2e

lint:
	uv run ruff check .

format:
	uv run ruff format .

clean:
	rm -rf artifacts/ local/ .context/ tmp/ __pycache__ .pytest_cache htmlcov .coverage
