.PHONY: run
run:
	docker compose -f docker-compose.prod.yml up -d

.PHONY: install
install:
	python3.11 -m venv venv
	. venv/bin/activate
	pip install -r requirements.txt

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
	docker compose -f docker-compose.test.yml run --rm test-api pytest
	docker compose -f docker-compose.test.yml down