# DevSecOps and secure secrets handling

## Security model

The project applies security checks before deployment rather than treating security as a final manual stage. Every push and pull request to `main` triggers a GitHub Actions workflow that scans Python source code with Bandit.

Workflow file:

```text
.github/workflows/security.yml
```

The pipeline:

1. checks out the repository;
2. starts an isolated GitHub-hosted runner;
3. installs Python 3.12 and Bandit;
4. recursively scans the `src/` directory;
5. fails when Bandit reports findings with medium-or-higher severity and medium-or-higher confidence.

Local equivalent:

```bash
python -m pip install bandit
bandit -r src -x tests -ll -ii
```

## Secrets

Real Telegram/VK tokens, passwords and network credentials must never be committed to Git.

The application reads runtime values from environment variables loaded from a local `.env` file with `python-dotenv`. The repository contains only `.env.example` with placeholder values.

Safe setup:

```bash
cp .env.example .env
chmod 600 .env
nano .env
```

Relevant protections:

- `.env` and `.env.*` are ignored by Git;
- `.env.example` is explicitly allowed as a sanitized template;
- bot code obtains credentials with `os.getenv(...)`;
- systemd services should load variables through `EnvironmentFile=`;
- CI does not require production bot tokens to run Bandit.

Before every push, verify tracked files:

```bash
git status
git ls-files | grep -E '(^|/)\.env($|\.)'
git grep -nEi '(token|password|secret|api[_-]?key)[[:space:]]*=[[:space:]]*["'\''][^"'\'']+'
```

Expected result: only the sanitized `.env.example` may be tracked, and no hard-coded credential should be found.

## Incident procedure for an exposed token

Removing a token from the latest file is not sufficient because it remains in Git history.

1. revoke or rotate the exposed token immediately;
2. replace it in the deployed environment;
3. remove the secret from the repository and history where required;
4. inspect forks, Actions logs, releases and artifacts;
5. document the incident without publishing the secret;
6. add a preventive check or rule.

## Current scope and limitations

Bandit is a SAST control for common Python security issues. It does not prove that the application is secure and does not replace dependency scanning, tests, code review, DAST, operating-system hardening or secure deployment configuration.

Recommended future additions:

- `pip-audit` for known vulnerable Python dependencies;
- `gitleaks` or GitHub secret scanning for credential patterns;
- Dependabot for dependency update pull requests;
- unit tests and linting in the same CI pipeline;
- DAST against a future web interface or API in an isolated test environment.