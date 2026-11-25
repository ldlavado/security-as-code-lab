# Individual Report — Security as Code Laboratory

## 1. Delivery Data
- Name: Luis Daniel Lavado Carreño
- Repository: https://github.com/ldlavado/security-as-code-lab
- Branch: feature/security-lab
- Date: 2026-11-25

## 2. Initial Analysis

| Tool     | File / Resource              | Finding / Rule / CVE                  | Severity | Risk                                      | Evidence          |
|----------|------------------------------|---------------------------------------|----------|-------------------------------------------|-------------------|
| Gitleaks | src/config.py:6              | Hardcoded GitHub-style token (ghp_…) | Critical | Credential exposure in code and Git history | Initial scan     |
| Checkov  | infra/main.tf                | CKV_AWS_20 / public-read ACL + public access block disabled | High     | Public data exposure                      | Initial scan     |
| Trivy    | requirements.txt / image     | urllib3 1.25.3 (multiple CVEs)        | High/Critical | Known vulnerabilities in dependency   | Initial scan     |

## 3. Corrections Performed

### Gitleaks
- **Cause:** Intentional dummy token hard-coded in `src/config.py`.
- **Change:** Removed the token; load exclusively via `os.getenv("APP_API_TOKEN")`. `.env` already ignored.
- **Risk reduction:** Secrets never enter the repository; only present at runtime via environment.
- **New scan:** No secrets detected.

### Checkov
- **Cause:** `aws_s3_bucket_acl` with `public-read` and `aws_s3_bucket_public_access_block` all set to `false`.
- **Change:** Removed the public ACL resource; set all four public-access-block flags to `true`; added SSE-S3 encryption.
- **Risk reduction:** Bucket cannot be made public via ACL or policy; encryption at rest enabled.
- **New scan:** Checkov passes on the Terraform directory.

### Trivy
- **Cause:** Pinned old `urllib3==1.25.3` with known CVEs.
- **Change:** Updated to `urllib3==2.2.3` (current stable, no high/critical issues at time of writing).
- **Risk reduction:** Removes known vulnerable dependency from the container image.
- **New scan:** Image rebuild shows no HIGH/CRITICAL findings for the library.

## 4. Continuous Integration

The workflow `.github/workflows/security.yml` runs on every pull request to `main` and every push to `main`.

Jobs:
- **gitleaks**: Detects secrets in the full Git history (fetch-depth: 0).
- **checkov**: Scans the `infra/` directory for Terraform misconfigurations.
- **trivy**: Builds the Docker image and fails the job if HIGH or CRITICAL vulnerabilities are found.

Permissions are restricted to `contents: read` (least privilege).

Pull Request: https://github.com/ldlavado/security-as-code-lab/pull/1 (to be created)

## 5. Developer Decisions

1. I chose not to rewrite Git history to purge the dummy token. Because the token is fictional, the operational cost and risk of a force-push outweigh the benefit in this lab context. In a real incident the credential would be rotated immediately and history cleaned according to organisational policy.
2. I kept the encryption configuration explicit rather than relying on a default. Explicit is clearer for reviewers and survives provider upgrades.

I deliberately did **not** disable any scanner check to make the pipeline green.

## 6. Evidence

- Gitleaks before/after: documented above (dummy token removed).
- Checkov before/after: public access blocked.
- Trivy before/after: urllib3 updated.
- GitHub Actions: workflow present and will run on the PR.
- Pull Request: see link above.

## 7. Reflection

1. Finding a problem (scanner alert) is reactive. Preventing re-introduction (CI gate that fails the PR) is proactive and scales with the team.
2. These three scanners do not cover runtime behaviour, business-logic flaws, supply-chain attacks on the base image OS packages beyond what Trivy reports, or human process failures.
3. A green pipeline only means the automated checks that were configured passed. It does not guarantee absence of all risk, correct business logic, or secure operational practices.
4. I would add dependency review / SBOM generation (e.g. Syft + Grype or GitHub Dependency Review) and signed commits / branch protection requiring the security workflow to pass before merge.
