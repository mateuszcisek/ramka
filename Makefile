env:
	poetry install

format:
	poetry run isort src/ tests/ examples/
	poetry run black src/ tests/ examples/

lint:
	./scripts/run_linting.sh

test:
	./scripts/run_tests.sh

example-sample-routes:
	PYTHONPATH=./src poetry run gunicorn --reload examples.sample_routes.app:app

shell:
	PYTHONPATH=./src poetry run ipython --pprint --color-info
