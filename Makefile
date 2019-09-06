cov-report = true

install:
	pip install -e .[aioredis,dev]

lint:
	black -l 100 --check aiorate_limiter tests
	flake8 aiorate_limiter _example
	mypy aiorate_limiter

format:
	black -l 100 aiorate_limiter tests _example

test:
	 coverage run -m pytest tests
	@if [ $(cov-report) = true ]; then\
    coverage combine;\
    coverage report;\
	fi