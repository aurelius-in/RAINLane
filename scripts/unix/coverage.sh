#!/usr/bin/env bash
set -euo pipefail
python -m pip install coverage
coverage run -m pytest -q
coverage html
coverage report -m

