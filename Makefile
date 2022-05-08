env:
	poetry install

format:
	poetry run isort src/ tests/
	poetry run black src/ tests/

lint:
	./scripts/run_linting.sh

test:
	./scripts/run_tests.sh

example:
	PYTHONPATH=./src poetry run gunicorn --reload src.web_framework_example.sample_app:app

shell:
	PYTHONPATH=./src poetry run ipython --pprint --color-info
