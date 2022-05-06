env:
	poetry install

test:
	poetry run pytest

example:
	PYTHONPATH=./src poetry run gunicorn --reload src.web_framework_example.sample_app:app
