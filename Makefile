# Makefile

install:
	pip install -r requirements.txt

test:
	python -m coverage run -m pytest -rP
	python -m coverage report
	python -m coverage html
