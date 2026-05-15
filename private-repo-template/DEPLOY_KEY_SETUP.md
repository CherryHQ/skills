# Deploy Key Setup (Detailed)

The sync workflow needs to push from your **private repo** to **CherryHQ/skills**. GitHub Actions can't do this with a normal PAT without giving your private repo access to all your repos. A deploy key is the cleanest solution: it's an SSH key that only works on one repo.

---

## Step 1: Generate the key pair (on your local machine)

Open terminal and run:

```bash
ssh-keygen -t ed25519 -C "skills-sync" -f ~/.ssh/skills-sync
```

When it asks for a passphrase, **just press Enter twice** (leave it empty). GitHub Actions can't type passphrases.

You'll get two files:
- `~/.ssh/skills-sync` — **private key** (never share, never commit)
- `~/.ssh/skills-sync.pub` — **public key** (safe to share)

Verify they exist:

```bash
ls ~/.ssh/skills-sync*
```

Expected output:
```
/Users/you/.ssh/skills-sync
/Users/you/.ssh/skills-sync.pub
```

---

## Step 2: Add the public key to CherryHQ/skills (public repo)

1. Open https://github.com/CherryHQ/skills/settings/keys (or go to repo → Settings → Deploy keys)

2. Click **"Add deploy key"**

3. Fill in:
   - **Title**: `Private repo sync`
   - **Key**: paste the entire contents of `~/.ssh/skills-sync.pub`
   
   To get the contents:
   ```bash
   cat ~/.ssh/skills-sync.pub
   ```
   It looks like:
   ```
   ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAID... skills-sync
   ```

4. ✅ **Check "Allow write access"** — this is critical, the workflow needs to push

5. Click **"Add key"**

---

## Step 3: Add the private key to your private repo's secrets

1. Open your **private repo** on GitHub

2. Go to **Settings → Secrets and variables → Actions**

3. Click **"New repository secret"**

4. Fill in:
   - **Name**: `PUBLIC_REPO_DEPLOY_KEY`
   - **Secret**: paste the entire contents of `~/.ssh/skills-sync`
   
   To get the contents:
   ```bash
   cat ~/.ssh/skills-sync
   ```
   It looks like:
   ```
   -----BEGIN OPENSSH PRIVATE KEY-----
   b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
   ...
   -----END OPENSSH PRIVATE KEY-----
   ```

5. Click **"Add secret"**

---

## Step 4: Verify the workflow file references the right secret

In your private repo, check `.github/workflows/sync-to-public.yml` has this line:

```yaml
ssh-key: ${{ secrets.PUBLIC_REPO_DEPLOY_KEY }}
```

If your secret name is different, update either the secret name or the workflow file to match.

---

## Step 5: Test

1. Make a small, harmless change to a skill that's in `publish-manifest.json`:
   ```bash
   # In your private repo
   echo "# test" >> skills/test-and-report/SKILL.md
   git add .
   git commit -m "Test sync workflow"
   git push origin main
   ```

2. Go to your **private repo** → Actions tab

3. You should see the "Sync Skills to Public Repo" workflow running

4. If it succeeds:
   - Go to **CherryHQ/skills** → Pull requests
   - You should see a new PR titled "Sync skills from private repo"
   - Review it, then merge

---

## Troubleshooting

| Problem | Likely cause | Fix |
|---------|-------------|-----|
| Action fails with "Permission denied" | Deploy key not added to public repo, or write access not enabled | Re-check Step 2 |
| Action fails with "Invalid key" | Secret copied incorrectly (extra spaces, missing headers) | Re-copy from `cat ~/.ssh/skills-sync`, don't use `pbcopy` on macOS if it adds formatting |
| No PR created | `create_pr_instead_of_push: false` in manifest, or commit step found no changes | Check manifest setting; verify your change actually modified a file in the skill directory |
| Workflow doesn't trigger | File path doesn't match `paths:` filter in workflow | Ensure you changed a file inside `skills/` directory |

---

## Security notes

- **Never** commit `skills-sync` (private key) to any repo
- **Never** share the deploy key secret with anyone who shouldn't be able to push to CherryHQ/skills
- If someone leaves the team, rotate the key: generate a new one, replace both the deploy key and the secret, delete the old key files
- The deploy key only works on `CherryHQ/skills` — it can't access any other repo
