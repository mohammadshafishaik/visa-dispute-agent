.PHONY: install test run docker-up docker-down seed-db migrate clean

install:
	poetry install

test:
	poetry run pytest -v

test-property:
	poetry run pytest tests/property_tests/ -v

test-unit:
	poetry run pytest tests/unit/ -v

test-coverage:
	poetry run pytest --cov=app --cov-report=html --cov-report=term

run:
	poetry run uvicorn app.api.main:app --reload --host 0.0.0.0 --port 8000

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down -v

seed-db:
	poetry run python scripts/seed_chromadb.py

migrate:
	poetry run alembic upgrade head

migrate-create:
	poetry run alembic revision --autogenerate -m "$(message)"

format:
	poetry run black app/ tests/
	poetry run ruff check --fix app/ tests/

lint:
	poetry run black --check app/ tests/
	poetry run ruff check app/ tests/
	poetry run mypy app/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov/ .hypothesis/

setup: install docker-up migrate seed-db
	@echo "Setup complete! Run 'make run' to start the server."
