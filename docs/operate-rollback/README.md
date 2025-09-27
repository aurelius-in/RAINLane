# Operate & Rollback SOP

- Operate: Argo CD sync with pinned digests; observe health; watch p95 latency
- Rollback: `argocd app rollback rainlane <REV>`; ensure traffic drains; verify smoke tests
- Incident: capture AnswerCard IDs and provenance, attach to ticket
