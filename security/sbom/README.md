# SBOM

- Generate: Syft in CI writes `artifacts/sbom.spdx.json`
- Scan: Grype fails build on critical vulnerabilities
- Store: keep generated SBOMs under `artifacts/` (gitignored)
