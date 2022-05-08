#!/bin/bash

set -e

files_with_test=$(find . -path "**/tests/**" -name "test_*.py" | sort)

if [ -z "${files_with_test}" ]; then
    echo "No tests have been found."
    exit 0
fi

echo "Running all tests from the following files:"
printf "%s\n\n" "${files_with_test}"

# shellcheck disable=SC2086
poetry run pytest -v ${files_with_test}
return_code=$?

if [ "$return_code" = 5 ]; then
  echo "No tests collected. Exiting with 0 (instead of 5)."
  exit 0
fi

exit "$return_code"
