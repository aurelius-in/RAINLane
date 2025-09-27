# RMODP: Roles, Models, Observability, Deployment, Policy

- Roles: Operator, Supervisor, QA, Engineering
- Models: task-aware selection via `service/model_selector/model_registry.yaml`
- Observability: OTEL traces, Prometheus metrics (stubs)
- Deployment: KServe + Argo CD with pinned digests
- Policy: OPA/Conftest gate on resources and cosign verification


