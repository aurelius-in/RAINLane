# Secrets

- Store provider keys in GitHub Actions secrets (e.g., `AZURE_OPENAI_*`, `ANTHROPIC_API_KEY`)
- Cosign keys: `COSIGN_PRIVATE_KEY`, `COSIGN_PASSWORD`, `COSIGN_PUBLIC_KEY`
- Consider sealed-secrets or cloud KMS for cluster-side configs
