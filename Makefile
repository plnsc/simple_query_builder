# Makefile

install:
	@echo "installing..."
	pip install -r requirements.txt

test:
	@echo "running tests..."
	python -m coverage run -m pytest -rP
	@echo "generating coverage reports..."
	python -m coverage report
	@echo "building html files from coverage reports..."
	python -m coverage html
