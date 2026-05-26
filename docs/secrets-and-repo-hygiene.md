# Secrets and repository hygiene

## Local Maps demo keys

The optional script `mapping/map_toy.py` uses the **Google Maps Platform** APIs (not Gemini). Prefer an environment variable:

```bash
export GOOGLE_MAPS_API_KEY='your-key'
```

Or copy `data_external/apikey.txt.example` to `data_external/apikey.txt` locally. Never commit `apikey.txt` or any Gemini / Generative Language API keys.

## If a key ever appeared in git history

Deleting the credential in Google Cloud stops **new** abuse but does **not** remove strings from clones or forks. After rotating the key in GCP, purge the paths from history and force-push (coordinate with anyone who clones the repo):

```bash
pip3 install --user git-filter-repo
python3 -m git_filter_repo --path data_external/apikey.txt \
  --path data/apikey.txt --invert-paths --force
git remote add origin https://github.com/jlillywh/Aegis.git   # filter-repo strips remotes; re-add your URL
git push --force --all origin
git push --force --tags origin
```

Verify nothing obvious remains:

```bash
git log --all -p -S 'AIza' --oneline
```
