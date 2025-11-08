.PHONY: install install-dev test lint format clean build run-web docker-build docker-run help

help:
	@echo "Available commands:"
	@echo "  make install      - Install production dependencies"
	@echo "  make install-dev  - Install development dependencies"
	@echo "  make test         - Run tests with coverage"
	@echo "  make lint         - Run linters (flake8, mypy)"
	@echo "  make format       - Format code with black"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make build        - Build the package"
	@echo "  make run-web      - Run the web UI"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt -r requirements-dev.txt

test:
	pytest

lint:
	flake8 src tests
	mypy src

format:
	black src tests

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .coverage htmlcov/
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

build:
	python setup.py sdist bdist_wheel

run-web:
	python -m wallet_card.web.app

docker-build:
	docker build -t wallet-card-generator -f docker/Dockerfile .

docker-run:
	docker-compose -f docker/docker-compose.yml up

