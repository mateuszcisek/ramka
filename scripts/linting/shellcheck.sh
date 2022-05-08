#!/bin/bash

echo "Running shellcheck..."

files_to_check=$(find . -name '*.sh' | sort)

if [ -z "${files_to_check}" ]; then
    echo "No files to check found."
    exit 0
fi

echo "Checking the following files:"
printf "%s\n" "${files_to_check}"

# shellcheck disable=SC2086
poetry run shellcheck ${files_to_check}
return_code="$?"

if [ "$return_code" != 0 ]; then
  printf "\U274C shellcheck found linting issues!\n\n"
  exit "$return_code"
else
  printf "\U1F680 shellcheck finished without issues!\n\n"
fi
