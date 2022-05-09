#!/bin/bash

echo "Running isort..."

poetry run isort --check-only src/ tests/ examples/
return_code="$?"

poetry run isort src/ tests/ examples/

if [ "$return_code" != 0 ]; then
  printf "\U274C isort found linting issues!\n\n"
  exit "$return_code"
else
  printf "\U1F680 isort finished without issues!\n\n"
fi
