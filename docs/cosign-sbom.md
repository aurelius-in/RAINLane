# Cosign + SBOM

- SBOM: Syft writes `artifacts/sbom.spdx.json`
- Scan: Grype fails build on criticals
- Sign and verify container digests with cosign
- CI pins the digest into kustomization
