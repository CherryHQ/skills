# Sync Template (Private Repo)

Copy these files into your **private** repository to enable automated skill sync to `CherryHQ/skills`.

## Files

| File | Purpose |
|------|---------|
| `publish-manifest.json` | Lists which skills to publish |
| `.github/scripts/sanitize-rules.json` | Replacement rules for branding & secrets |
| `.github/scripts/sanitize.py` | Runs the actual cleaning |
| `.github/workflows/sync-to-public.yml` | GitHub Actions workflow |

## Setup Steps

### 1. Copy files to your private repo

```bash
# In your private repo root
cp -r private-repo-template/* .
git add .
git commit -m "Add sync workflow for public skill publishing"
```

### 2. Generate Deploy Key

```bash
ssh-keygen -t ed25519 -C "skills-sync" -f skills-sync.key
# Leave passphrase empty
```

### 3. Add deploy key to public repo

Go to **CherryHQ/skills** → Settings → Deploy keys → Add deploy key
- Paste contents of `skills-sync.key.pub`
- ✅ **Allow write access**

### 4. Add private key to private repo secrets

Go to **your private repo** → Settings → Secrets and variables → Actions → New repository secret
- Name: `PUBLIC_REPO_DEPLOY_KEY`
- Value: full contents of `skills-sync.key`

### 5. Edit `publish-manifest.json`

List only the skills you want public:

```json
{
  "skills": [
    "test-and-report",
    "prd-creator"
  ]
}
```

### 6. Edit `.github/scripts/sanitize-rules.json`

Add any new product names, internal URLs, or secret patterns. The workflow will fail if it detects un-replaced secrets.

### 7. Test

Push a change to any skill in the manifest:

```bash
git add skills/test-and-report/SKILL.md
git commit -m "Test sync"
git push origin main
```

Check the Actions tab in your private repo. It should create a PR (or direct push, depending on `create_pr_instead_of_push` setting) in `CherryHQ/skills`.

## How It Works

1. **Trigger**: Push to `main` branch in private repo, or manual run
2. **Copy**: Only skills listed in `publish-manifest.json` are copied
3. **Sanitize**: `sanitize.py` runs replacement rules on every file
4. **Remove**: Files matching `exclude_from_public` patterns are deleted
5. **Push**: Changes land in public repo (direct push or PR)

## Safety

- **Secret detection**: If `base_token` or `table_id` patterns remain after sanitization, the workflow logs warnings
- **Exclusion list**: Internal docs/credentials never leave private repo
- **PR mode (default)**: `create_pr_instead_of_push: true` opens a PR for human review before merging

## Changing Behavior

Edit `publish-manifest.json`:

```json
{
  "skills": ["test-and-report"],
  "create_pr_instead_of_push": true,   // set false for fully auto
  "auto_merge": false                  // not yet implemented
}
```
