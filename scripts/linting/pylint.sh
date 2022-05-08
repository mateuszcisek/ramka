#!/bin/bash

echo "Running pylint..."

poetry run pylint src/ tests/
return_code="$?"

if [ "$return_code" != 0 ]; then
  printf "\U274C pylint found linting issues!\n\n"
  exit "$return_code"
else
  printf "\U1F680 pylint finished without issues!\n\n"
fi
