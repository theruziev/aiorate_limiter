cov-report = true

install:
	pip install -e .[redis,dev]

lint:
	black -l 100 --check rate_limiter tests
	flake8 rate_limiter

format:
	black -l 100 rate_limiter/ tests/

test:
	 coverage run -m pytest tests
	@if [ $(cov-report) = true ]; then\
    coverage combine;\
    coverage report;\
	fi