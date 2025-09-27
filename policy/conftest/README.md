# Conftest

- Policies live in `policy/opa`
- Run: `conftest test serve/rollouts/rainlane-api.yaml -p policy/opa`
- CI workflow enforces deny rules for images, signatures, resource limits
