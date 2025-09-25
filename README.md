# RAINLane

**Certified answers, fast.**
Answer operational and compliance questions from SOPs with structure-aware ingestion, green/yellow routing, task-aware model selection, signed provenance, and a red-team harness for safety.

## Outcomes

* Trustworthy, explainable answers with verifiable provenance
* Lower latency and cost by choosing the right model per task
* Clear separation of certified vs advisory responses
* Continuous safety via red-team attack suites and policy gates

## What’s inside

* **Ingestion:** PDF to section/paragraph chunks, table capture, content hashing
* **Routing:** **Green** (certified) and **Yellow** (advisory) lanes with deterministic policies
* **Model Selector:** task classification to pick model and prompt profile with reason codes
* **Provenance Notary:** signed AnswerCards with citations, hashes, model/version
* **Serving:** KServe InferenceService, Argo CD apps with pinned digests, rollouts and rollback
* **Evals:** accuracy, hit\@k, p95 latency, cost per answer, certified coverage
* **Red-Team Harness:** prompt injection, exfil, role bypass, and hallucination traps

## AI agents

* **Query Router:** applies policy rules and user training levels to choose lane and retrieval profile
* **Model Selector:** maps request type to provider and prompt profile, records `selector_reason`
* **Provenance Notary:** attaches citations, hashes, model/version and signs the AnswerCard
* **Gold-Question Curator:** validates SME-submitted certified Q\&A and generates regression tests

## Architecture

```
Docs (PDF/SOP/Policy)
   │
   ▼
Ingestion → Structure-Aware Chunking → Indexes (vector + keyword)
                                │
User Query ─▶ Query Router ─▶ Model Selector ─▶ Green Lane (certified)
                                │
                                └────────────────▶ Yellow Lane (advisory)
                                                     │
                                             Provenance Notary → AnswerCard (signed)
                                                     │
                                           Evals & Red-Team Reports
```

## Repository layout

```
/ingest/{pdf,chunking,hashing,policies}
/service/{api,schemas,provenance,model_selector,model_registry.yaml}
/green-lane/{gold-questions,rules,tests}
/yellow-lane/{fallback,disclaimers,escalation}
/evals/{harness,metrics,reports}
/serve/{kserve,rollouts}
/gitops/{apps,overlays}
/redteam/{attacks,runners,reports}
/ci/.github/workflows
/docs/{rmodp,traceability,operate-rollback,outcomes}
```

## API (FastAPI)

* `POST /v1/ingest` → upload a document, returns section count and content hashes
* `POST /v1/answer` → `{query, user_role}` → returns `AnswerCard` with lane, citations, hashes, signature, `selector_reason`
* `GET  /v1/provenance/{answer_id}` → full chain: doc versions, spans, model, policy, signature
* `POST /v1/gold/submit` → submit/update certified questions with schema checks and tests

### `AnswerCard` (schema excerpt)

```json
{
  "id": "ans_...",
  "lane": "green|yellow",
  "answer": "string",
  "citations": [{"doc_id":"...","section":"4.2","span":[120,198]}],
  "doc_hashes": [{"doc_id":"...","sha256":"..."}],
  "model": {
    "name":"...",
    "version":"...",
    "selector_reason":"task=table_lookup; rule=has_table"
  },
  "signature": {"key_id":"...", "sig":"..."},
  "metrics": {"latency_ms": 420, "cost_usd": 0.003}
}
```

## CI/CD and safety

* CI: unit tests, schema checks for gold questions, SBOM, cosign sign and verify
* Serving: KServe with autoscaling; Argo CD with pinned digests, optional canary
* Red-Team: weekly runs of injection/exfil/role-bypass suites, signed report, CI fails on criticals
* Secrets: Sealed Secrets or Key Vault; NetworkPolicies and RBAC examples

## Evals and reporting

* `make evals` produces JSON metrics and a PDF report in `/evals/reports`
* Metrics: certified accuracy, retrieval hit\@k, p95 latency, cost per answer, certified coverage
* Red-Team reports in `/redteam/reports` with example prompts and fixes

## Observability

* OpenTelemetry traces for ingestion, routing, selection, retrieval, generation, notarization
* Prometheus metrics with Grafana dashboards: coverage, accuracy, latency, cost, blocked attempts, red-team trends

## KPIs

* Certified coverage (%) and certified accuracy (%)
* p95 latency (ms) and cost per answer (USD)
* Dispute/override rate
* Blocked attempt rate and time to patch red-team findings
* Time to certify a new question

## Getting started

```bash
make init
make ingest path=./docs/sop-changeover.pdf
make run.local
curl -s localhost:8000/v1/answer \
  -H "Content-Type: application/json" \
  -d '{"query":"What is the sterile changeover checklist?","user_role":"Operator"}'
make evals
make redteam.run
```

## Configuration

* `service/model_registry.yaml` for task→model routing
* Env vars or secrets for providers, signing keys, and storage backends
* Optional: enable canary via Argo Rollouts in `/serve/rollouts`

## Roadmap

* Model A/B holdout for selector win-rate
* SME review UI for gold questions
* Adaptive retrieval profiles per document family

---
