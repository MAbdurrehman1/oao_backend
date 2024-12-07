#!/usr/bin/env bash

set -o errexit  # this line is for returning an error whenever the script exits with non-zero state
source .venv/bin/activate
mypy .
