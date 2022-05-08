#!/bin/bash

declare -a scripts=(
    "scripts/linting/pylint.sh"
    "scripts/linting/black.sh"
    "scripts/linting/isort.sh"
    "scripts/linting/shellcheck.sh"
)

# shellcheck disable=SC2034
declare -a results=()
result=0

for script in "${scripts[@]}"
do
    bash "$script"
    exit_code=$?
    result=$((result + exit_code))
done

if [ "$result" = 0 ]; then
    printf "\U1F680 \e[1m\e[32mAll checks passed!\e[0m\n"
    exit 0
fi

printf "\n\U274C \e[1m\e[31mCommit failed due to linting issues,"
printf " see the log \e[97m\U2B06\U2B06\U2B06\e[0m\n"
exit "$result"
