SHELL := /bin/bash
run.local:
	uvicorn service.api:app --reload --port 8000
ingest:
	curl -s -X POST localhost:8000/v1/ingest -H 'Content-Type: application/json' -d '{"path":"./docs/sop.txt"}' | jq
answer:
	curl -s -X POST localhost:8000/v1/answer -H 'Content-Type: application/json' -d '{"query":"what is the sterile changeover checklist?","user_role":"Operator"}' | jq
evals:
	python evals/harness/run.py
redteam.run:
	python redteam/runners/run_redteam.py
test:
	pytest -q
fmt:
	black . && isort .
lint:
	black --check . && isort --check-only .
precommit:
	pre-commit run --all-files || true


