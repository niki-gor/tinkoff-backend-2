.PHONY: run
run:
	python -m forum

.PHONY: install
install:
	python3.11 -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt

.PHONY: swagger
swagger:
	python -m webbrowser http://localhost:8000/docs 