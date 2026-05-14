# Cherry Studio Skills

A shared Claude Code skills repository for the Cherry Studio team. Not tied to any single product line — Cherry Studio desktop client, Cherry Studio Enterprise, internal tools, day-to-day workflows. If a workflow can be packaged as a skill, it belongs here.

> 👐 **Everyone is welcome to contribute skills they've refined.**
> A good skill = one person figures out the workflow + the whole team saves time forever. Everything from "write my weekly report" and "polish copy" to "system testing collaboration" and "code review" is worth capturing.

Structure follows [anthropics/skills](https://github.com/anthropics/skills).

---

## Current Skills

| Skill | Purpose | Typical Triggers |
|-------|---------|------------------|
| [test-and-report](skills/test-and-report/) | Accompany users through manual staging testing, file bugs to a Feishu Bitable + GitHub issue dual-track system | `test and report` / `start system testing` / `help me test cherry / express saas` / paste Feishu test doc + bitable |
| [prd-creator](skills/prd-creator/) | Discuss a Cherry Studio community-edition requirement with PM → produce a bilingual PRD review → after user confirmation, create the English GitHub issue (CherryHQ/cherry-studio) + auto-add to Project #3 + set fields | `create requirement` / `draft an issue` / `new feature issue` / `draft an issue for...` |
| [transcript-to-content](skills/transcript-to-content/) | Turn transcripts, meeting recordings, or raw notes into publishable content: multiple social posts or a single long-form article. Auto-verifies proper nouns, numbers, and ASR errors; long articles use an index-retrieval strategy to prevent hallucination | `write an article` / `turn this talk into a blog post` / `write up this session` / `convert transcript` |
| [expense-reimbursement](skills/expense-reimbursement/) | Full lifecycle expense reimbursement: single invoice intake, batch aggregation, approval workflow, ledger and dashboard | `expense` / `invoice` / `reimbursement` / `submit expense` |

_(Keep adding to this table.)_

---

## Use Cases

| Scenario | Examples |
|----------|----------|
| Product workflows | Client / SaaS testing, releases, PR review, doc collaboration |
| Engineering workflows | Issue triage, PRD writing, code review, release notes generation |
| Ops / Marketing / PM | Weekly reports, meeting notes, WeChat post formatting, Feishu group notifications |
| Daily office work | Email drafting, schedule organizing, Feishu Bitable automation |
| Onboarding | Environment setup guides, internal repo access requests, knowledge-base indexing |

If you do it repeatedly and it's slightly painful every time, it's a skill candidate.

---

## Installation (pick one)

### Option 1: Symlink a single skill (recommended)

Lightweight. Clone the repo, then symlink the skill you want into `~/.claude/skills/`:

```bash
cd ~/code  # wherever you keep code
git clone git@github.com:CherryHQ/skills.git
cd skills

# Enable a specific skill
ln -s "$(pwd)/skills/test-and-report" ~/.claude/skills/test-and-report
```

Updates come through `git pull`.

### Option 2: Symlink all skills

```bash
cd ~/code/skills
for skill in skills/*/; do
  name=$(basename "$skill")
  ln -sfn "$(pwd)/$skill" ~/.claude/skills/"$name"
done
```

### Option 3: Copy (no auto-updates)

```bash
cp -R skills/test-and-report ~/.claude/skills/
```

After installation, invoke the skill in Claude Code / Conductor using its trigger phrases.

---

## Prerequisites (most skills need these)

| Capability | Check | If Missing |
|------------|-------|------------|
| `lark-cli` | `lark-cli contact +get-user` returns current user | Follow internal onboarding docs for `lark-shared` auth |
| `gh` CLI | `gh auth status` shows logged in with write access to target repos | `gh auth login` + ask org admin to add you to repos |
| `upload-img` (Cloudflare R2 image hosting) | `which upload-img` returns `~/.local/bin/upload-img` | Ask internal ops for the script, or use manual upload as fallback |
| `claude-in-chrome` extension (for testing / browser skills) | Claude icon visible in Chrome menu and shows "Connected" | Install from [claude.com/chrome](https://claude.com/chrome) |

---

## Adding a New Skill (PRs welcome ❤️)

1. **Prototype locally first** — build it in `~/.claude/skills/<name>/`, iterate until it works smoothly
2. **Drop it in `skills/<name>/`** — directory name must match the `name` in SKILL.md frontmatter
3. **Must include `SKILL.md`** with YAML frontmatter containing `name` + `description` (description is the core of trigger logic)
4. **Optional**: `references/` (long procedures / configs), `scripts/` (executables), `assets/` (templates / icons)
5. **Add a row to the "Current Skills" table** in this README
6. Open a PR

**Tips** (fewer surprises):
- Use Anthropic's `skill-creator` skill to draft + optimize descriptions — trigger accuracy improves significantly
- Keep SKILL.md under 500 lines; long content goes into `references/`, linked from SKILL.md
- Write clearly "**when to use**" and "**when NOT to use**" in the description (negative lists prevent false triggers)
- If a skill references base_tokens / private repo names / internal URLs, be mindful of confidentiality (this repo is private, but don't copy to public repos)

**Not sure what to build?** High-value directions:
- Package any workflow you've done 5+ times manually (weekly reports, schema changes, email replies)
- Turn team FAQs of "how do I do X" into callable skills
- Wrap an external CLI / API with a convenience layer

---

## Collaboration Conventions

- **Naming**: kebab-case, verb-first (`test-and-report`, `doc-review`, `wechat-crm`)
- **Changes**: PRs go through review, merges use squash
- **Deprecation**: Mark unused skills with `[DEPRECATED]` in their description rather than deleting — gives teammates time to adjust
- **Breaking changes**: Write a CHANGELOG entry; if trigger phrases change, flag it in the PR description

---

## Confidentiality Notice

This is an **internal / private** repository. Skills may contain staging tokens, internal repo names, customer data schemas, account open_ids, and other sensitive information.

- ❌ Do NOT copy skills to public repositories
- ❌ Do NOT quote skill configuration blocks verbatim on public channels (X / WeChat / blogs)
- ✅ Sharing, discussing, and learning from skills inside the company is encouraged
