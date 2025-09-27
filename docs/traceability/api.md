# API Examples

Ingest:

```bash
curl -s -X POST localhost:8000/v1/ingest -H 'Content-Type: application/json' -d '{"path":"./docs/sop.txt"}'
```

Answer:

```bash
curl -s -X POST localhost:8000/v1/answer -H 'Content-Type: application/json' -d '{"query":"what is the sterile changeover checklist?","user_role":"Operator"}'
```
