# Bug Submission SOP (Bitable + GitHub Issue Dual-Track)

This document is the detailed procedure for the `test-and-report` skill Phase 4. Every bug must complete all 6 steps in order, without skipping.

---

## 1. Entry Prerequisites

Before entering this SOP, ensure you have an "evidence package":

- One-sentence symptom description (user's own words)
- Trigger conditions / reproduction steps
- Environment info (OS / browser / version / login status)
- At least one piece of objective evidence (screenshot / Console error / network request / DOM state)
- (Optional) code-level root cause

If evidence is incomplete → return to Phase 3 to fill gaps. Do NOT enter the SOP with partial evidence.

---

## 2. Dedup (Mandatory, 5-Category Disposition)

### 2.1 Extract Keywords

Pick the most specific 2-3 keywords from the symptom (error code, component name, function name, file path, key stack trace). **Do NOT** search with the full sentence.

### 2.2 Search 3 Sources

**① Feishu Bitable:**
```
lark-cli base +record-search --base-token <BASE> --table-id <TABLE> --json '{"keyword":"<keyword>","search_fields":["Issue Title","Issue Description","Notes"],"limit":20}'
```

**② GitHub issues (open + closed):**
```
gh issue list --repo <OWNER/REPO> --search '<keyword>' --state all --limit 20
```

**③ GitHub PRs (open + merged):**
```
gh pr list --repo <OWNER/REPO> --search '<keyword>' --state all --limit 10
```

### 2.3 Apply 5-Category Disposition

Compare side-by-side (symptom / trigger / platform / version), classify into one:

| Verdict | Evidence | Action |
|---------|----------|--------|
| **Identical open entry** | Symptom+trigger+platform nearly identical, issue/record not closed | **Do NOT create new**. Tell user "already tracked in #xxx / record <id>", ask whether to append info or cancel |
| **Fixed issue regression** (closed `✅fixed`) | Symptom identical but issue closed with fix label | **Possible regression**. Tell user "#xxx was fixed in vX.X but symptom reappears — possible regression", wait for user to decide: create new or append to old issue |
| **In-progress PR** (open or merged but not released) | PR clearly references related code/issue, not yet in current environment | Tell user "PR #yyy is already in progress, expected vX.X"; user can: create tracking entry, wait for release, or comment on the PR |
| **Related but different** | Symptom similar but trigger/module/impact clearly different | Can create new, but **must cross-reference** (Bitable note `see #xxx`, issue body `Related: #xxx`) |
| **Unrelated** | No search hits | Proceed to Section 3 normally |

### 2.4 Output Format

After searching, present a summary table to the user:

```
Related search results:

Bitable:
| record_id | Title | Status | Relation |
| ...       | ...   | ...    | ...      |

GitHub Issue:
| #   | Title | Status | Relation |
| ... | ...   | ...    | ...      |

GitHub PR:
| #   | Title | Status | Relation |
| ... | ...   | ...    | ...      |

Recommendation: {Create new | Append to existing | Wait for PR release}
Rationale: ...
```

**Iron rule**: Show the table and recommendation to the user in all cases, **wait for explicit instruction before acting**. Even if no hits, ask "No related entries found. Confirm creating new?" — never decide unilaterally.

---

## 3. Assign Priority (P0 / P1 / P2)

### 3.1 Three-Tier Definitions

| Tier | Definition | Response Time |
|------|-----------|---------------|
| **P0** | Main path blocked / feature completely broken / data loss / security flaw | **Must fix immediately** |
| **P1** | Serious experience issue, main path still works but clearly degraded | Fix soon (current sprint) |
| **P2** | Minor experience issue / very infrequent edge case | Queue for later |

### 3.2 Decision Rules

1. **Inferable from symptom** (user said "can't proceed", "crash", "data lost", etc.) → fill directly + briefly explain in Phase 4 Step 6 report so user can override
2. **Not inferable** → **must** use `AskUserQuestion` with P0/P1/P2 options, prompt text:

   > What's the priority of this bug?
   > - P0: Main path blocked, must fix immediately
   > - P1: Serious experience issue, fix soon
   > - P2: Minor issue / infrequent edge case, queue for later

3. **Strictly forbidden** to default to P1 or guess randomly — pollutes metrics and scheduling

---

## 4. Upload Screenshots to Cloudflare R2

```bash
upload-img <local-path-to-screenshot>
# Returns https://pub-a9416c5573a34388b8d9465d8bef4257.r2.dev/YYYYMMDD/<filename>
```

- Script location: `~/.local/bin/upload-img`
- Bucket: `screenshots`
- Key format: `YYYYMMDD/<original-filename>` (date prefix auto-added)
- Returns a **public URL**, embed directly in GitHub issue or share

Upload images one at a time, embed URLs in issue body individually.

---

## 5. Write to Feishu Bitable

### 5.1 Create Record

```bash
lark-cli base +record-upsert \
  --base-token <BASE> \
  --table-id <TABLE> \
  --json '<record_json>'
```

**Required fields**:

| Field | Value Format | Example |
|-------|-------------|---------|
| Issue Title | text (≤40 chars summary) | `"Login page send-code button disabled on first load"` |
| Issue Description | text (multi-line, symptom+env+steps+impact) | `"Symptom: ...\nEnvironment: ...\nSteps: 1) ... 2) ..."` |
| Issue Category | select (single) | `"Bug"` or `"UX Improvement"` |
| Priority | select (single) | `"P0"` / `"P1"` / `"P2"` |
| Status | select (single) | **New submissions default `"Pending Confirmation"`** — don't change to later states |
| Submitter | user | `[{"id":"ou_xxxxxx"}]`, obtained via `lark-cli contact +get-user --jq .data.user.open_id` |

**Optional fields**: `Module` (Desktop App has 17 options, SaaS Platform currently only "Other") / `Issue` (URL, write as `[#xxx](url)` format, table shows #xxx short link) / `Owner` (user) / `Notes` (multi-line) / `Example Image` (**don't put here**, see below)

**Do NOT write**: `Created At` (system auto)

### 5.2 Value Format Quick Reference

| Field Type | JSON Value |
|-----------|------------|
| text | `"string"` (supports `\n` newlines) |
| select (single) | `"P0"` (string, exact match to option name) |
| user | `[{"id":"ou_xxx"}]` |
| text(url) | Recommended `"[#129](https://.../issues/129)"` — column shows clickable #129; also accepts plain URL `"https://..."` |
| attachment | **Use separate API** `+record-upload-attachment` |
| created_at / updated_at | Do not write |

### 5.3 Upload Attachments

**Cannot** go through upsert. After getting record_id, call separately:

```bash
lark-cli base +record-upload-attachment \
  --base-token <BASE> \
  --table-id <TABLE> \
  --record-id <record_id> \
  --field-id <example_image_field_id> \
  --file <local-path> \
  --name <display-name>   # optional, defaults to filename
```

Call once per image.

### 5.4 Pitfalls

- `jq` path for record_id is `.data.record.record_id_list[0]`, **not** `.data.record.record_id` (which is null)
- Single-select values are case-sensitive (`"p0"` fails, must be `"P0"`)
- User fields use `{id: ...}` wrapped in array, not bare string

---

## 6. Create GitHub Issue

### 6.1 Title Format

- Category = Bug → `[Bug]: <one-sentence summary>`
- Category = UX Improvement → `[Feature]: <one-sentence improvement summary>` or `[Enhancement]: <...>`

### 6.2 Body Format (follow `<OWNER>/<REPO>#<ISSUE_NUMBER>`)

```markdown
> [!NOTE]
> This issue was written in English by Claude. Original Chinese content is at the bottom.

### Pre-submission Checklist

- [x] I have searched existing issues and did not find a duplicate.
- [x] I have written a short, specific title.
- [x] I have provided reproduction information and root-cause analysis.

### Environment

- **URL**: <staging URL>
- **Branch**: `<branch>`
- **Commit**: `<short sha>` (as of <date>)
- **Platform**: <OS / browser>

### Summary

<One paragraph: symptom + reproducibility>

<img width="675" alt="<describe>" src="<R2 public URL>" />

### Root Cause

<Analysis with file:line references, code blocks for critical snippets>

### Why it races / Why it fails

<Mechanism explanation>

### Proposed Fix

<Tabular form preferred when changes map cleanly to rows (i18n keys, field copy, config values, enum additions):>

| Field | Label | Description | Placeholder |
|---|---|---|---|
| ... | ... | ... | ... |

<Otherwise a short numbered list of behavioral changes.>

**Files to touch:**
- `<path>:<line-range>` — <what changes>

### Out of scope

<Bulleted list of adjacent questions intentionally deferred (separate issue / product decision). Keeps this issue's scope bounded and prevents reviewers from expanding it.>

### Reproduction

<Step-by-step; include DevTools throttle settings if relevant>

### Related files

- `<file>:<line>` — <what's there>

---

<details>
<summary>Original Chinese Content</summary>

### Phenomenon
...

### Root Cause
...

### Proposed Fix
...

### Out of Scope
...

### Reproduction
...

</details>
```

### 6.3 Create Command

```bash
gh issue create --repo <OWNER/REPO> \
  --title '<title>' \
  --body-file <path-to-body.md>
```

### 6.4 Add Labels

**Check repo's existing labels first**, then decide what to use — don't invent `type:*` namespaces blindly:

```bash
gh label list --repo <OWNER/REPO> --limit 100
```

Priority for label selection:

1. **Reuse existing label**: if repo has `bug` / `feature` / `BUG` / `enhancement` with matching semantics, use it directly.
   ```bash
   gh issue edit <N> --repo <OWNER/REPO> --add-label "<existing>"
   ```
2. **Only create new when no semantic match**:
   ```bash
   gh label create "type: bug" --color "d73a4a" --description "Functional defect (bitable: Bug)" --repo <OWNER/REPO>
   gh label create "type: feature" --color "0366d6" --description "UX improvement (bitable: UX Improvement)" --repo <OWNER/REPO>
   ```

**Known repo conventions**:
- `<REPO_A>` (public desktop client): uses legacy `BUG`/`feature`/`P1`-`P3`, do NOT create `type:*`.
- `<REPO_B>` (private SaaS API): currently uses `bug` / `feature` (see #135). Check `gh label list` before creating `type:*`.

**Priority labels** (optional):
- `<REPO_A>` has existing `P1` / `P2` / `P3` labels. Bitable P0/P1/P2 map to P1/P2/P3 or add `P0` separately.
- `<REPO_B>` currently has no priority labels; check `gh label list` before creating.

### 6.5 Backfill Issue URL to Bitable

```bash
lark-cli base +record-upsert \
  --base-token <BASE> \
  --table-id <TABLE> \
  --record-id <record_id> \
  --json '{"Issue": "[#<N>](<issue URL>)"}'
```

---

## 7. Report Back to User

Fixed format:

```
✅ Submitted

Title: <issue title>
Category: <Bug | UX Improvement>  Priority: <P0 | P1 | P2>  Status: Pending Confirmation
record_id: <rec_xxx>
Issue: <GitHub issue URL>
Bitable: <base URL?table=tbl_xxx>

(Priority rationale if applicable): <one sentence>
```

On failure, expose error code + raw error message. Do not hide it.

---

## 8. Common Errors Quick Reference

| Error | Cause | Fix |
|-------|-------|-----|
| `[800004135] OpenAPI* limited` | Feishu API rate limit | `sleep 2-5` then retry, add delay between consecutive calls |
| `[1254045]` field name doesn't exist | Option name typo (`p0` vs `P0`) | `+field-list` to check actual option names |
| `[1254066]` user field error | Wrote plain string or forgot `{id: ...}` | Change to `[{"id":"ou_xxx"}]` |
| Write succeeded but example image empty | Attachments can't go through upsert | Use `+record-upload-attachment` |
| `gh label create` 404 | No triage/write permission | Ask user to grant permission to current GH account |
| `gh issue create` succeeded but no label | Same as above | Create label first, then retry `edit --add-label` |
| JS tool `Cannot access a chrome-extension:// URL of different extension` | Page has cross-extension iframe (Geetest etc.) | Fall back: `read_page` + read source |
