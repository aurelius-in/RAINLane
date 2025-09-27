#!/usr/bin/env bash
set -euo pipefail
q="${1:-what is the sterile changeover checklist?}"
role="${2:-Operator}"
curl -s -X POST http://127.0.0.1:8000/v1/answer -H 'Content-Type: application/json' -d "{\"query\":\"$q\",\"user_role\":\"$role\"}" | jq .

