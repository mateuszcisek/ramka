#!/bin/bash

echo "Running black..."

poetry run black --check src/ tests/ examples/
return_code="$?"

poetry run black src/ tests/ examples/

if [ "$return_code" != 0 ]; then
  printf "\U274C Some files were reformatted by black!\n\n"
  exit "$return_code"
else
  printf "\U1F680 black finished without issues!\n\n"
fi
