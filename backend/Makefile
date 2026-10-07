.PHONY: up down logs build test lint ps restart clean

up:
	docker compose up --build -d

down:
	docker compose down

restart:
	docker compose down && docker compose up --build -d

logs:
	docker compose logs -f --tail=200

ps:
	docker compose ps

build:
	docker compose build

test:
	pytest tests/ -v

lint:
	ruff check services workers shared tests

clean:
	docker compose down -v
