#!/usr/bin/env bash
set -euo pipefail
id="$1"
curl -s "http://127.0.0.1:8000/v1/provenance/$id" | jq .

