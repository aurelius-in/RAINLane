#!/usr/bin/env bash
set -euo pipefail
path="${1:-./docs/sop.txt}"
curl -s -X POST http://127.0.0.1:8000/v1/ingest -H 'Content-Type: application/json' -d "{\"path\":\"$path\"}" | jq .

