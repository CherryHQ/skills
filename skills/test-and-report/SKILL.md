---
name: test-and-report
description: Manual testing + bug filing for Enterprise / SaaS products. Parses a Feishu test doc (scope + repo + bitable URL), observes staging via claude-in-chrome, captures DOM/console/network/screenshot evidence, then dual-tracks each finding — Feishu Bitable record (with attachments) + GitHub issue (<REPO>#<ISSUE_NUMBER> format — English-primary, Chinese collapsed, R2-hosted screenshots, matching type label). Enforces dedup across bitable + GitHub issues + PRs, and mandatory P0/P1/P2 priority prompt when unclear. Trigger whenever the user says "test and report", "test and report side-by-side", "start system testing", "experience staging", "collaborate on bug filing", "collect feedback", a shared Feishu testing doc, a bitable URL + finding, or any UX/bug needing both bitable + GitHub tracking. Do NOT use for writing product code, PR review, CI debugging, or general "how do I use this product" questions — those go to normal dev / PR-review / support flows.
---

# Test & Report

A skill that packages the full flow: "Feishu test doc → browser evidence capture → dual-track submission (Bitable + GitHub issue)" so every piece of feedback includes environment info, screenshots, dedup conclusion, and priority, tracked in two systems.

## Trigger Boundaries (when to use / when not to use)

**Use this skill:**
- User sends a Feishu test doc URL (usually contains test scope + code repo + Bitable link)
- User says "start testing / help me test / experience staging / collab on bugs / collect feedback"
- User describes a UX / functional issue and wants it tracked in both Bitable + GitHub
- User sends a known test Bitable URL (e.g. `IJQPbTzZhaObMQsuL5OcbaoBnag` / `AdeDbC9VgaNkrEsXtk5cTMarn2e`) with feedback

**Do NOT use this skill:**
- User asks you to write product code / open a PR → use normal dev flow
- User asks you to review an existing PR → use `gh-pr-review` skill
- CI / build failure debugging → use normal debugging
- User asks "how do I use this product / where do I download" → general answer

---

## Prerequisites (check before executing)

| Capability | Check Method | If Missing |
|------------|-------------|------------|
| claude-in-chrome extension | `mcp__claude-in-chrome__tabs_context_mcp` returns tab list | Guide user to install from claude.com/chrome and click Connect, wait for "done" |
| lark-cli logged in | `lark-cli contact +get-user --jq .data.user.name` | Jump to `lark-shared` skill for auth |
| gh CLI has repo write access | `gh api repos/<OWNER>/<REPO> --jq .permissions` shows `push: true` | Ask user to grant triage/write to current GitHub account |
| R2 image hosting available | `which upload-img` returns `~/.local/bin/upload-img` | Manual fallback: ask user to drag screenshot into GitHub issue editor |

## Workflow Overview

```
Phase 1  Parse test doc (Feishu doc → config)
Phase 2  Browser setup (claude-in-chrome)
Phase 3  Accompany testing: user operates, agent observes
Phase 4  Per-bug submission (dedup → priority → upload screenshot → Bitable + GitHub dual-track)
Phase 5  Return to Phase 3 until user says "done"
```

---

## Phase 1: Parse Test Document

User provides a Feishu document URL. Use `lark-cli docs +fetch --doc <URL> --format pretty` to pull full text, then extract:

| Config Item | Usually Found In |
|-------------|-----------------|
| **Test topic / scope** | Title + opening paragraphs |
| **Code repository** (GitHub URL) | "Reference repo" / "Code repository" section, or GitHub link in body |
| **Staging URL** | "Test environment" / "Access URL" section |
| **Issue collection Bitable** | "Issue collection" / "Bug list" section with `mcnnox2fhjfq.feishu.cn/wiki/...?table=tbl...` or `/base/...?table=tbl...` |

**If user only gives a Bitable URL without a document**: identify the product (see auto-detection rules below), use the config from `references/bitable-bases.md`, and ask user for the staging URL if not found in the Bitable first record.

### Auto-detect Current Product

Use these signals to determine which product, and therefore which repo + Bitable to use:

| Signal | Product | Repository | Bitable |
|--------|---------|------------|---------|
| URL contains `cse-admin-staging.cherry-ai.com` / `enterprise-api` / "SaaS" / "Enterprise" | **Enterprise / SaaS** | `<ENTERPRISE_REPO>` | `IJQPbTzZhaObMQsuL5OcbaoBnag` / `tbl20SIk4B78Ydpg` |
| Mentions "client" / "desktop" / Electron | **Desktop Client** | `<DESKTOP_REPO>` | `AdeDbC9VgaNkrEsXtk5cTMarn2e` / `tbl7eUvrbfM7XFqg` |
| Neither clear | Ask user | — | — |

Known config details (field IDs, enum values, view shortcuts) are in `references/bitable-bases.md`.

---

## Phase 2: Browser Setup

1. `tabs_context_mcp { createIfEmpty: true }` to check connection
2. If not connected → guide user to install claude-in-chrome extension (claude.com/chrome), click Connect, retry
3. Once connected, `navigate` to staging URL
4. Do a baseline capture before any bug is reported:
   - `read_page --filter interactive` for main interactive elements
   - `read_console_messages` / `read_network_requests` start recording
   - (Optional) note core script sources (third-party captcha / CDN / analytics)

**Tool pitfalls:**
- `javascript_tool` may throw `Cannot access a chrome-extension:// URL of different extension` when page loads cross-extension iframes (e.g. Geetest). Fall back to `read_page` + reading source.
- `read_console_messages` / `read_network_requests` need to be listening from page load — refresh once before reading.
- Don't use `chrome-devtools` MCP debug features simultaneously — they'll conflict with claude-in-chrome for Debugger protocol access.

---

## Phase 3: Accompany Testing Loop

User operates manually. Agent does two things:

1. **Passive observation**: don't drive the user, don't click randomly
2. **On-demand support**: when user says "there's a problem / can't click / error / looks wrong", immediately collect evidence

**Evidence package** (collect for every bug):

| Dimension | Tool | Key Points |
|-----------|------|------------|
| Phenomenon description | User's own words | One sentence + reproduction trigger |
| DOM state | `read_page`, `javascript_tool` | Check disabled / pointerEvents / opacity / event listeners |
| Console errors | `read_console_messages --pattern 'error\|warn\|Error'` | Keep only error/warn, not everything |
| Network anomalies | `read_network_requests --urlPattern '<api-prefix>'` | Look for 4xx/5xx/pending |
| Screenshots | Ask user cmd+shift+4 to `.context/attachments/`, or `mcp__chrome-devtools__take_screenshot` | Required for error scenes; for UX issues, "current vs expected" is better |
| Code root cause | `gh api` / local grep | If source is available, find button enable conditions / API paths / props gates |

Once evidence is complete, proceed to Phase 4.

---

## Phase 4: Per-Bug Submission

Detailed procedure in `references/submit-bug-sop.md`. **High-level steps** (don't skip):

1. **Dedup** (mandatory, see SOP Section 2)
   - Search Bitable + GitHub issues (including closed) + GitHub PRs (including merged)
   - On hit, apply 5-category disposition: identical / fixed regression / in-progress PR / related but different / unrelated
   - Show comparison table to user, wait for instruction — **confirm even when no hit**

2. **Assign priority** (see SOP Section 3)
   - If inferable from symptoms → fill directly + brief rationale
   - If not inferable → `AskUserQuestion` with P0/P1/P2 options
   - **Never** default to P1 or guess randomly

3. **Upload screenshot to R2** (see SOP Section 4)
   ```
   upload-img <local-path>
   # Returns https://pub-a9416c5573a34388b8d9465d8bef4257.r2.dev/YYYYMMDD/filename
   ```

4. **Write to Feishu Bitable**
   - `+record-upsert` required: issue title / description / category / priority / status (=pending confirmation) / submitter
   - `+record-upload-attachment` attach screenshot to the "Example image" field (**do not** stuff into upsert)

5. **Create GitHub issue**
   - Title: `[Bug]: <one sentence>` or `[Feature]: <one sentence>` (based on category)
   - Body follows generic issue format: English body first (with translation disclaimer), Chinese original collapsed in `<details>`, screenshots embedded as `<img src="...">` with R2 URLs
   - Labels: category = Bug → `type: bug`; = UX improvement → `type: feature`

6. **Report back**: give user record_id, issue URL, and Bitable URL together, plus a summary: "title / category / priority / status"

---

## Phase 5: Return to Phase 3

User continues testing. Every bug report goes through Phase 4.

When user says "done / finished / pause for today / stop" → output session summary: how many records created, how many issues filed, which regressions / in-progress PRs were identified, total time spent.

---

## Reference Files

- `references/bitable-bases.md` — Known Base tokens / table IDs / field IDs / enum values, cross-base field naming conventions
- `references/submit-bug-sop.md` — Detailed submission protocol (5 dedup categories, priority rules, value formats, R2 upload, issue template)
