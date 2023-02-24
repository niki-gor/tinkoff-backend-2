.PHONY: run
run:
	uvicorn forum:app --reload

.PHONY: tmp
tmp:
	uvicorn example:app --reload

.PHONY: init
init:
	python -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt