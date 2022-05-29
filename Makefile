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

documentation:
	rm -r docs/build
	poetry run sphinx-build docs/source docs/build

documentation-examples:
	rm -r docs/source/content/source_code
	poetry run sphinx-apidoc -o docs/source/content/source_code src/ramka

documentation-source-code:
	rm -r docs/source/content/example_projects
	poetry run sphinx-apidoc -o docs/source/content/example_projects examples/
