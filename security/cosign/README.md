# Cosign

- Sign: `cosign sign --key env://COSIGN_PRIVATE_KEY <image>@<digest>`
- Verify: `cosign verify --key env://COSIGN_PUBLIC_KEY <image>@<digest>`
- CI pins digest into `gitops/overlays/dev/kustomization.yaml`
