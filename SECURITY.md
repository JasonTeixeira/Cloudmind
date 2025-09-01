# Security Policy

## Supported Versions
We currently support the latest main branch for security updates.

## Reporting a Vulnerability
- Report privately to security@cloudmind.local
- Include reproduction steps and impact
- We acknowledge within 48 hours and provide a remediation ETA

## Repository Practices
- Secrets are never committed; use `.env` (gitignored) with `env.example`
- CI runs Trivy, Bandit, npm audit; Python deps audited with pip-audit
- Sensitive dirs (`keys/`, `storage/`) are gitignored
- Security headers and auth toggles are controlled via environment variables

## Hardening Checklist
- Rotate `SECRET_KEY` and all API keys regularly
- Enforce MFA and least-privilege for all cloud credentials
- Keep dependencies updated and audited
- Run security tests regularly (`backend/tests/test_phase4.py`)
