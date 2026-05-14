# Cherry Studio Skills

A shared Claude Code skills repository for the Cherry Studio team and community. Not tied to any single product line — Cherry Studio desktop client, Cherry Studio Enterprise, internal tools, day-to-day workflows. If a workflow can be packaged as a skill, it belongs here.

> 👐 **Everyone is welcome to contribute skills they've refined.**
> A good skill = one person figures out the workflow + the whole team saves time forever.

Structure follows the [Agent Skills specification](https://agentskills.io/specification) by [anthropics/skills](https://github.com/anthropics/skills).

---

## Quick Start

### Install via Claude Code Plugin

```bash
/plugin marketplace add CherryHQ/skills
/plugin install cherry-studio-skills@CherryHQ/skills
```

Or install individual skill groups:
```bash
/plugin install testing-skills@CherryHQ/skills
/plugin install content-skills@CherryHQ/skills
```

### Manual Install (symlink)

```bash
cd ~/code
git clone git@github.com:CherryHQ/skills.git
cd skills

# Enable a specific skill
ln -s "$(pwd)/skills/test-and-report" ~/.claude/skills/test-and-report
```

### Using in Claude.ai / API

Upload the skill folder directly. See [Using skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude).

---

## Skill Catalog

### 🧪 Testing & Quality
| Skill | Purpose | Triggers |
|-------|---------|----------|
| [test-and-report](skills/test-and-report/) | Manual staging testing + dual-track bug filing (Feishu Bitable + GitHub) | `test and report` / `start testing` / `staging review` / `file a bug` |

### 📝 Product & Content
| Skill | Purpose | Triggers |
|-------|---------|----------|
| [prd-creator](skills/prd-creator/) | Bilingual PRD drafting → English GitHub issue creation with Project #3 integration | `create requirement` / `draft an issue` / `new feature issue` |
| [transcript-to-content](skills/transcript-to-content/) | Transcripts → social posts or long-form articles. Style learning, fact-checking, ASR correction | `write an article` / `turn this talk into a blog post` / `convert transcript` |

### 💼 Operations
| Skill | Purpose | Triggers |
|-------|---------|----------|
| [expense-reimbursement](skills/expense-reimbursement/) | Full lifecycle: invoice intake → batch aggregation → approval → ledger & dashboard | `expense` / `invoice` / `reimbursement` / `submit expense` |

---

## Creating a Skill

Use the [template](template/SKILL.md) as a starting point:

```markdown
---
name: my-skill-name
description: A clear description of what this skill does and when to use it.
---

# My Skill Name

[Instructions that Claude follows when this skill is active]

## Examples
- Example usage 1
- Example usage 2

## Guidelines
- Guideline 1
- Guideline 2
```

For complex skills, see [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) from Anthropic for the full eval-and-iterate workflow.

### Skill Structure

```
skills/<name>/
├── SKILL.md              # Required. YAML frontmatter + instructions
├── README.md             # Optional. Human-readable overview
├── references/           # Optional. Long procedures, configs, standards
│   └── *.md
├── scripts/              # Optional. Executable helpers
│   └── *.py
├── agents/               # Optional. Sub-agent definitions for complex workflows
│   └── *.md
├── evals/                # Optional. Test cases
│   └── *.json
└── assets/               # Optional. Templates, images, icons
    └── *
```

### Frontmatter Requirements

| Field | Required | Description |
|-------|----------|-------------|
| `name` | ✅ | Unique kebab-case identifier |
| `description` | ✅ | When to trigger + what it does. This is the primary triggering mechanism — include both positive triggers ("use when...") and negative triggers ("do NOT use when...") |

### Tips

- **Description is everything**: Claude decides whether to load your skill based solely on the `description` field. Be specific about trigger contexts.
- **Keep SKILL.md under 500 lines**: Long content goes into `references/`, linked from SKILL.md.
- **When to use / when NOT to use**: Negative trigger lists prevent false activations.
- **Include worked examples**: A concrete example prevents more misinvocations than pages of abstract rules.
- **Version your references**: If a skill has persistent state (like style profiles), document the storage format.

---

## Contributing

1. Prototype locally in `~/.claude/skills/<name>/`
2. Copy to `skills/<name>/` in this repo
3. Add to the Skill Catalog table in this README (pick the right category)
4. Open a PR

### Naming Conventions

- Directory names: `kebab-case`, verb-first (`test-and-report`, `doc-review`, `wechat-crm`)
- PRs go through review, merges use squash
- Breaking changes: write a CHANGELOG entry; if trigger phrases change, flag in PR description

---

## Prerequisites (most skills need these)

| Capability | Check | If Missing |
|------------|-------|------------|
| `lark-cli` | `lark-cli contact +get-user` returns current user | Follow internal onboarding docs |
| `gh` CLI | `gh auth status` shows logged in with write access | `gh auth login` + ask org admin |
| `upload-img` (Cloudflare R2) | `which upload-img` returns `~/.local/bin/upload-img` | Ask internal ops for the script |
| `claude-in-chrome` extension | Claude icon visible in Chrome, "Connected" | Install from [claude.com/chrome](https://claude.com/chrome) |

---

## License

This repository is licensed under [Apache 2.0](LICENSE).

**Note**: Some skills reference internal tools, tokens, or URLs. These are documented for the Cherry Studio team. External contributors can adapt the patterns to their own infrastructure.

---

## Acknowledgments

Skill structure and conventions inspired by [anthropics/skills](https://github.com/anthropics/skills). The [Agent Skills specification](https://agentskills.io/specification) defines the open standard.
