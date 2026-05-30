# Security policy

How to report vulnerabilities in **SHRINE** and which releases receive security fixes. Roadmap **3.18**.

SHRINE is alpha research/engineering software. We take good-faith reports seriously even while the project is pre-1.0.

---

## Supported versions

Security fixes are applied to **supported** lines on `master` and released as patch versions when applicable.

| Version | Supported | Notes |
|---------|-----------|--------|
| `0.2.x` | **Yes** | Current alpha line; active development on `master` |
| `0.1.x` | **No** | Superseded by `0.2.0` |
| Pre-`0.1.0` | **No** | Not supported |

After the first PyPI release ([docs/pypi.md](docs/pypi.md)), this table will track the latest **MINOR** line (e.g. `0.2.x` while `0.3.0` is in development). See also [Supported versions](docs/releases.md#supported-versions) in the release guide.

---

## Reporting a vulnerability

**Do not** open a public GitHub issue for an undisclosed security vulnerability.

### Preferred: GitHub private reporting

1. Open **[Report a vulnerability](https://github.com/jlillywh/SHRINE/security/advisories/new)** (Repository → **Security** → **Advisories** → **Report a vulnerability**).
2. Describe the issue, impact, and steps to reproduce.
3. Include affected version(s) or commit hash if known.

GitHub keeps the report private while we investigate.

### Alternative: direct contact

If private advisories are unavailable, contact the maintainer privately:

- **[Jason Lillywhite](https://github.com/jlillywh)** — repository owner (`@jlillywh`)

Use GitHub’s private contact option or another channel the maintainer has shared with you. Do **not** paste exploit code or credentials into public issues, PRs, or discussions.

---

## What to include

Help us respond quickly:

| Item | Why it helps |
|------|----------------|
| Summary and suspected impact | Triage severity |
| Affected component (`shrine.simulation`, scenario loader, etc.) | Route to the right code path |
| Steps to reproduce or proof-of-concept | Confirm and fix |
| SHRINE version or `git` commit | Know what to patch |
| Your environment (OS, Python version) | Reproduce locally |

---

## Response expectations

| Stage | Target |
|-------|--------|
| Initial acknowledgment | Within **7 days** |
| Triage (severity, scope) | Within **14 days** when possible |
| Fix or mitigation plan | Depends on severity; we aim for critical issues on `master` promptly |

We may ask for clarification. If we decline a report (e.g. out of scope), we will explain why.

---

## Disclosure

- We coordinate with reporters before public disclosure when possible.
- Fixed issues are noted under **Security** in [CHANGELOG.md](CHANGELOG.md) and may be published as a [GitHub Security Advisory](https://github.com/jlillywh/SHRINE/security/advisories).
- Please allow reasonable time for a patch before public disclosure (typically **90 days** for non-critical issues, shorter for critical issues by agreement).

---

## Scope

**In scope**

- Vulnerabilities in this repository’s code (framework, adapters, examples shipped in the repo)
- Unsafe defaults in scenario loading, file I/O, or export paths that enable injection or arbitrary code execution **through SHRINE APIs**

**Out of scope**

- Vulnerabilities in **dependencies** (report to upstream; we will bump versions when fixes exist)
- Issues in **legacy domain modules** with no supported public entry point, unless reachable from `shrine.simulation` without intentional misuse
- Social engineering, physical security, or denial-of-service against maintainer infrastructure
- Findings in **unreleased** or unsupported versions with no practical upgrade path

---

## Secrets in the repository

If you find an **exposed API key or credential** in the repo or history, treat it as sensitive: report privately and do **not** post the secret value. See [docs/secrets-and-repo-hygiene.md](docs/secrets-and-repo-hygiene.md).

---

## Related

- [CONTRIBUTING.md](CONTRIBUTING.md) — general contribution workflow
- [GOVERNANCE.md](GOVERNANCE.md) — maintainer and release roles
- [docs/releases.md](docs/releases.md) — versioning and supported lines
- [Code of Conduct](CODE_OF_CONDUCT.md)
