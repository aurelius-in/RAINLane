#!/usr/bin/env bash
set -euo pipefail
tail -f artifacts/openapi.json || echo "Use container logs or uvicorn output"

