#!/usr/bin/env bash
set -euo pipefail
uvicorn service.api:app --reload --port 8000
