# Security as Code Lab — Solution

This repository demonstrates a small Python application and Terraform configuration that have been hardened according to Security as Code principles.

The original intentional findings (hardcoded secret, public S3 bucket, vulnerable dependency) have been corrected. Continuous security scanning is enforced via GitHub Actions.

> This is a laboratory solution. Do not deploy the example resources to a real cloud account.

## What was fixed

| Area | Before | After |
|------|--------|-------|
| Secrets | Hardcoded dummy token in `src/config.py` | Loaded only from `APP_API_TOKEN` environment variable |
| Infrastructure | S3 bucket with public-read ACL and public access enabled | Public access fully blocked + server-side encryption |
| Dependencies | `urllib3==1.25.3` (known CVEs) | `urllib3==2.2.3` |
| CI | Workflow present | Same workflow now passes on the corrected code |

Detailed analysis, decisions and reflection are in [`docs/INFORME.md`](docs/INFORME.md).

## Repository structure

```
.
├── .github/workflows/security.yml   # Gitleaks + Checkov + Trivy on every PR
├── docs/INFORME.md                  # Completed lab report
├── infra/main.tf                    # Hardened S3 bucket
├── src/
│   ├── app.py
│   └── config.py                    # Environment-only configuration
├── Dockerfile
├── requirements.txt
└── evidence/                        # Place for scan screenshots
```

## Run the application

```bash
export APP_API_TOKEN="local-placeholder-value"
python src/app.py
```

## Run the scanners locally

```bash
# Secrets
gitleaks dir .
gitleaks git .

# Infrastructure as Code
checkov -d ./infra

# Container image
docker build -t security-as-code-lab:local .
trivy image --scanners vuln --severity HIGH,CRITICAL security-as-code-lab:local
```

## Continuous Integration

The workflow in `.github/workflows/security.yml` runs on pull requests and pushes to `main`:

- **gitleaks** – secret detection (full history)
- **checkov** – Terraform misconfiguration scan
- **trivy** – container image vulnerability scan (fails on HIGH/CRITICAL)

Permissions are limited to `contents: read`.

## Conventional Commits

All changes on `feature/security-lab` follow the [Conventional Commits](https://www.conventionalcommits.org/) specification.

---

Original lab instructions (for reference) can be found in the upstream repository:  
https://github.com/AndUm423/security-as-code-lab
