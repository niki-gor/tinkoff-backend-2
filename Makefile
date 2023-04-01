.PHONY: run
run: up

.PHONY: install
install:
	docker compose -f docker-compose.prod.yml build --no-cache

.PHONY: lint
lint:
	black .

.PHONY: swagger
swagger:
	python -m webbrowser http://localhost:8081/docs 

.PHONY: up
up:
	docker compose -f docker-compose.prod.yml up --build -d
.PHONY: down
down:
	docker compose -f docker-compose.prod.yml down

.PHONY: test
test:
	docker compose -f docker-compose.test.yml run --build --rm test-api pytest
	docker compose -f docker-compose.test.yml down