# Secrets and repository hygiene

**Audience:** Contributors and maintainers  
**Goal:** Keep API keys, tokens, and credentials out of Git history and off GitHub.

---

## Never commit

| Item | Why |
|------|-----|
| `**/apikey.txt` (except `*.example` templates) | Historically held Google API keys |
| `.env`, `.env.*` | Local environment overrides |
| `venv/`, `.venv/` | Environment-specific; large |
| Raw credentials in scenarios, notebooks, or test fixtures | Scanners and forks copy history forever |

`.gitignore` enforces most of this. **Ignoring a file does not remove it from past commits** — see [If a key was committed](#if-a-key-was-committed) below.

---

## Storing secrets locally

### Preferred: environment variables

For the optional Maps demo (`mapping/map_toy.py`):

```bash
export GOOGLE_MAPS_API_KEY='your-maps-platform-key'
python mapping/map_toy.py
```

Use a **Google Maps Platform** key (Elevation API, etc.). Do **not** use a Gemini / Generative Language API key for this script.

### Alternative: local file (gitignored)

```bash
cp data_external/apikey.txt.example data_external/apikey.txt
# Edit apikey.txt — one line, no quotes. File stays local only.
```

`data_external/` is ignored except `apikey.txt.example`, which is a template with no real secret.

---

## Choosing the right Google credential

| Use case | Credential type |
|----------|-----------------|
| `mapping/map_toy.py` (elevation, gmplot) | Maps Platform API key |
| LLM / Gemini experiments | Separate key; **not** used by SHRINE core |
| Production automation | Service account or OAuth where appropriate; never commit JSON keys |

Restrict keys in [Google Cloud Console](https://console.cloud.google.com/apis/credentials) (API restrictions, HTTP referrers, quotas).

---

## Automated scanning (CI and local)

| Layer | What runs |
|-------|-----------|
| **GitHub Actions** | [`.github/workflows/secrets.yml`](https://github.com/jlillywh/SHRINE/blob/master/.github/workflows/secrets.yml) runs **gitleaks** on every push/PR to `master` |
| **Pre-commit (optional)** | [`.pre-commit-config.yaml`](https://github.com/jlillywh/SHRINE/blob/master/.pre-commit-config.yaml) scans **staged** files before each commit |
| **Manual** | `./scripts/scan_secrets.sh` (requires [gitleaks](https://github.com/gitleaks/gitleaks) installed) |

Config and allowlists (docs, `apikey.txt.example`): [`.gitleaks.toml`](https://github.com/jlillywh/SHRINE/blob/master/.gitleaks.toml).

### Enable pre-commit locally

Use the project venv (do not `pip install` into system Python on Ubuntu — PEP 668 blocks it):

```bash
cd SHRINE
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
```

Run on all files once (uses the hook’s staged/pre-commit mode over the repo):

```bash
pre-commit run gitleaks --all-files
```

If you see `cannot change to 'protect'`, update `.pre-commit-config.yaml` — the upstream hook uses `gitleaks git --pre-commit`, not `gitleaks protect`.

---

## Before you push

Quick self-check from the repo root:

```bash
git status
git diff --cached | grep -iE 'api[_-]?key|secret|password|AIza[0-9A-Za-z_-]{20,}' || true
pre-commit run gitleaks --all-files   # if pre-commit is installed
```

If anything looks like a key, **stop**, rotate the credential in the provider, and do not push until the commit is fixed.

---

## If a key was committed

1. **Revoke or delete** the credential in the provider (e.g. GCP) immediately.
2. **Remove** it from the working tree and ensure `.gitignore` covers the path.
3. **Purge history** (coordinate with anyone who has cloned the repo):

```bash
pip3 install --user git-filter-repo --break-system-packages   # if needed on Debian/Ubuntu
python3 -m git_filter_repo --path data_external/apikey.txt \
  --path data/apikey.txt --invert-paths --force
git remote add origin https://github.com/jlillywh/Aegis.git   # filter-repo removes remotes; re-add yours
git push --force-with-lease origin master
git push --force-with-lease origin <other-branch>   # every branch that had the secret
```

4. **Verify** locally:

```bash
git log --all --oneline -- data_external/apikey.txt data/apikey.txt   # should be empty
git log --all -p -S 'AIza' --oneline   # may list this doc only (example commands), not key blobs
```

5. **Re-clone** or `git fetch` + `git reset --hard origin/master` on other machines.
6. **Resolve** any GitGuardian / GitHub secret scanning alerts after the force-push.

Forks and old clones may retain old objects until they fetch rewritten history or delete the fork.

---

## Reporting a leaked secret

If you discover a secret in this repository (current tree or history), contact the maintainers privately. Do not open a public issue with the key value.

---

## Related docs

- [testing.md](testing.md) — what not to commit with test runs (`venv/`, local data)
- [modernization-roadmap.md](modernization-roadmap.md) — Phase 0 security tasks
