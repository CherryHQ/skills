---
name: prd-creator
description: Discuss a Cherry Studio community-edition product requirement with the user, draft a bilingual (Chinese + English) PRD for review, then — after explicit user approval — create the English-only issue on GitHub (CherryHQ/cherry-studio). Use whenever the user wants to turn a requirement (from a Feishu doc, a meeting note, a customer ask, or a rough idea) into a GitHub issue. Triggers on phrases like "建需求单", "create a requirement", "把这个需求建到 GitHub", "新建 feature issue", "draft an issue for...", or anytime the user describes a Cherry Studio feature/improvement they want tracked. The format is opinionated (Background / Goal / Spec / Verification / Related, NO implementation details, draft shown bilingually for human review, issue itself written in English only).
---

# Cherry Studio Requirement Issue (PRD)

This skill helps a PM and an AI agent collaborate on a Cherry Studio requirement, draft it bilingually for review, and only then publish the English version as a GitHub issue. The issues are read by both human developers and Claude Code, so the body sticks to product logic plus concrete verification cases — **never implementation details**.

## How this skill works

The skill is a **conversation**, not a one-shot generator. The flow is:

1. **Discuss** — user describes a requirement (often roughly). Agent asks clarifying questions if needed.
2. **Verify before drafting** — agent reads the linked feedback issues and grep's the repo to ground Background in real product state, not assumptions.
3. **Draft bilingually** — agent produces a draft in Chinese + English side-by-side, so the user (Chinese-speaking PM) can review fluently.
4. **Iterate with cross-section consistency** — when one section changes, agent proactively checks whether sibling sections need updating too.
5. **Publish English-only** — once confirmed, agent creates the GitHub issue using only the English version. The Chinese gloss is review-only and does NOT enter the issue body.

## Why this format

- **Pure product logic, no code**: The PRD describes WHAT and WHY in product terms. HOW (file paths, libraries, data structures, code patterns) is left entirely to engineers and Claude Code at implementation time.
- **Spec + Verification, complementary not redundant**: Spec describes the rules (declarative). Verification gives concrete inputs/outputs and edge cases that prove the rules hold. If a Verification bullet 1:1 mirrors a Spec bullet, it's noise — delete it.
- **Concise**: 5 sections only. No "Out of Scope" (unless explicitly called out by the user), no traditional QA-style "Acceptance Criteria", no team assignments.
- **Bilingual draft, English issue**: PM reviews in Chinese (catches nuance fast); Claude Code and international contributors consume the published issue in English.
- **Linked feedback**: Real user-reported issues (`#xxxx`) ground the requirement in actual pain.

## The template (English — what gets published)

```markdown
## Background

(1-3 sentences. The user pain. Why does this need to exist? Concrete scenarios beat abstractions — name the symptom users see. Must reflect verified product state, not guessed behavior.)

## Goal

(One sentence. The product outcome — what users will be able to do after this ships.)

## Spec

(3-6 bullets. The product-level logic, written as user-observable behavior — the *rules*. Each bullet is a behavior the product exhibits. NO file paths, NO data structures, NO library names, NO "use Redux", NO "modify X.ts".)

## Verification

(3-8 bullets. Concrete *instances* that prove the Spec works. Different from Spec — Spec is rules, Verification is specific cases. Focus on:
- Specific input → expected observable output (named values, not abstract "X → Y")
- Multi-step sequences (first do A, then B, expect C)
- Edge cases: empty / very long / concurrent / offline / multi-window
- Negative checks (after X, Y should NOT happen)
- Target screenshot description for UI work — describe what the user sees, not which component renders it

If a Verification bullet 1:1 mirrors a Spec bullet, delete it. Verification stays at the product/UX level too.)

## Related

(Linked GitHub issues that report the same pain or are tangential. Format as `#1234 #5678 ...`. PRs go on a separate line prefixed `PRs:`.)
```

**Title format**: `[Feature]: <Title in Title Case>`

## Bilingual review format

When showing the user a draft, use this layout. English is the source of truth (it's what gets published); Chinese is the gloss for review.

```markdown
**Title (英)**: [Feature]: ...
**标题（中）**: ...

---

### Background / 背景

**EN:**
> ...

**中:**
> ...

### Goal / 目标

**EN:**
> ...

**中:**
> ...

### Spec / 具体逻辑

**EN:**
> - bullet 1
> - bullet 2

**中:**
> - 条目 1
> - 条目 2

### Verification / 验证

**EN:**
> - case 1

**中:**
> - 案例 1

### Related / 相关

#1234 #5678
```

End every draft with: **"确认这版就建到 GitHub。要改哪一句？"** (or English equivalent if the user is using English).

## Workflow

### 1. Discuss & gather input

If the user opens with a vague requirement, ask up to 3 clarifying questions before drafting. Useful questions:
- 背景细节：什么样的用户在什么场景下会遇到这个问题？
- 范围：这个需求是只覆盖 X，还是也包括 Y？
- 关联反馈：有哪些 social feedback / GitHub issue 是这个需求的来源？(if not provided, offer to search via `gh issue list --search`)
- Priority / Milestone — these go into Project #3 fields, NOT the issue body, but record them for later.

If the user already gives enough detail, skip questions and go straight to step 2.

### 2. Check for duplicates

```bash
gh issue list --repo CherryHQ/cherry-studio --search "<keyword from requirement>" --state all --limit 10
```

Also check Project #3:

```bash
gh api graphql -f query='query{organization(login:"CherryHQ"){projectV2(number:3){items(first:50){nodes{content{__typename ... on Issue{number title state}}}}}}}'
```

If a strong match exists, recommend **reusing** that issue (update its body) instead of creating new. Tell the user: "Issue #N already covers this — I suggest updating its body rather than creating a duplicate. Proceed with reuse?" Only create new if the user explicitly chooses to.

### 3. Verify before drafting (REQUIRED)

**Do this every time, even when the requirement looks obvious.** It catches misframings before they ship to GitHub.

For each issue in the user's "Related" list, read the actual content:

```bash
gh issue view <number> --repo CherryHQ/cherry-studio --json title,body
```

Look for:
- The actual user pain in the original report (not just the title)
- Existing workarounds users mention (these often reveal the real product gap)
- Closed issues with similar titles — read them too, they often contain the proposed-but-not-shipped solution
- Comments on related PRs

Then grep the cherry-studio repo for the feature area to verify current product state:

```bash
# Use Grep tool, not bash grep
# Search for keywords from the requirement to find the real constraint
```

Concrete failure mode this prevents: writing Background that says "users can't do X" when actually X works fine and the real problem is Y. The OpenAI/Anthropic interop PRD almost shipped with a generic "endpoint format mismatch" framing until verification revealed the real pain was Agent mode's hard dependency on Anthropic-format endpoints — a much sharper, more actionable framing.

If verification reveals facts the user didn't mention, surface them before drafting:
> "I read #13625 and the agent code — the real constraint is X, not Y as we discussed. Should I draft against that?"

### 4. Draft the bilingual version

Write English first (it's the source of truth), then mirror in Chinese for review.

Default examples / lexicon when concrete values are needed:
- **Aggregator provider example**: `CherryIN` (not OpenRouter — Cherry-first)
- **Frontier OpenAI model example**: latest available (e.g. `gpt-5.5` at time of writing — not `gpt-4o`, which is too old to be a credible Agent example)
- **Anthropic model example**: `Claude Sonnet` (most recent generation)
- **Gemini model example**: latest stable Gemini at time of writing
- If unsure what's "current", ask the user or grep `packages/aiCore/` for what's actively wired up

Stale or off-brand examples damage the document's credibility — readers calibrate trust on whether the PM/agent knows what shipped recently.

Keep these instincts in mind:
- **Background** describes the pain *users feel*, not the technical gap. "Users frequently hit X" beats "the system lacks Y".
- **Goal** is a single sentence about user-visible outcome.
- **Spec** bullets describe behavior at the product level — the *rules*. Free of implementation language.
- **Verification** bullets describe *specific cases*, not rules. Concrete enough to be mechanically checked.

### 5. Self-check before showing to user

Run this checklist mentally on every draft:

- [ ] **No code references**: Body contains no file paths, function names, library names, or framework references. (Common offenders: `src/`, `packages/`, `.ts`, `.tsx`, `useEffect`, `Redux`, `Drizzle`.)
- [ ] **Spec ≠ Verification redundancy**: For each Verification bullet, scan the Spec list. If any Verification bullet just rephrases a Spec rule with different words, delete it. Verification should add specifics (named inputs, edge cases, negative checks) that Spec doesn't already imply.
- [ ] **Examples are current**: Provider examples use CherryIN as primary; model examples are the latest generation, not legacy.
- [ ] **No filler**: Phrases like "provide a great user experience", "improve user satisfaction", "TBD", "more details to come" — strip them.

### 6. Iterate with cross-section consistency

When the user revises one section, **proactively** check whether sibling sections need updating before re-showing the draft.

Trigger questions to ask the user when appropriate:
- Background changed → "Background now emphasizes <new framing>. Should Goal or Spec be re-aligned to match?"
- Goal narrowed → "Goal now scopes to X only. Should we drop the Y bullets from Spec / Verification?"
- A new Verification case added that contradicts existing Spec → flag it: "this Verification bullet implies Spec needs another rule. Add it?"

Don't blindly carry old sections forward when the framing shifts. The OpenAI/Anthropic interop PRD went through exactly this — Background was sharpened (Agent unlock as primary pain), and Goal/Spec/Verification all needed re-pivoting to match.

Loop until explicit confirmation ("确认 / OK / 建吧 / yes ship it"). Don't auto-create on a single "looks good" — wait for an unambiguous "build it" signal.

### 7. Create the issue (English only)

Once confirmed, write the **English-only** body to a temp file and create:

```bash
cat > /tmp/req-body.md << 'BODY_EOF'
## Background
...
BODY_EOF

gh issue create --repo CherryHQ/cherry-studio \
  --title "[Feature]: <title>" \
  --body-file /tmp/req-body.md
```

If the user has already specified a milestone, add `--milestone "v2.1.0"`.

After creation, immediately add the issue to Project #3 and set its fields. This is part of the skill's job — do not leave it as "manual TODO for the user".

```bash
PROJECT_ID="PVT_kwDOCzFCf84A1VHU"
STATUS_FIELD="PVTSSF_lADOCzFCf84A1VHUzgq0WB4"
FEATURE_TODO_OPTION="78aaad35"
PRIORITY_FIELD="PVTSSF_lADOCzFCf84A1VHUzgq0WFk"
# Priority option IDs: P0=55393b39, P1=c2301f11, P2=dcd3a7ad

ISSUE_NODE=$(gh api repos/CherryHQ/cherry-studio/issues/<NUMBER> -q ".node_id")
ITEM_ID=$(gh api graphql -f query="mutation{addProjectV2ItemById(input:{projectId:"$PROJECT_ID",contentId:"$ISSUE_NODE"}){item{id}}}" -q ".data.addProjectV2ItemById.item.id")

gh api graphql -f query="mutation{
  s:updateProjectV2ItemFieldValue(input:{projectId:"$PROJECT_ID",itemId:"$ITEM_ID",fieldId:"$STATUS_FIELD",value:{singleSelectOptionId:"$FEATURE_TODO_OPTION"}}){projectV2Item{id}}
  p:updateProjectV2ItemFieldValue(input:{projectId:"$PROJECT_ID",itemId:"$ITEM_ID",fieldId:"$PRIORITY_FIELD",value:{singleSelectOptionId:"<PRIORITY_OPTION_ID>"}}){projectV2Item{id}}
}"
```

Then output the issue URL with a one-line confirmation: "Added to Project #3 with Status=Feature Todo, Priority=Px, Milestone=vX.Y.Z."

If the GraphQL call fails with a permissions error, ask the user to grant the current `gh` account Write access on Project #3, then retry. Do not silently fall back to "user does it manually" — that loses the workflow.

### 8. Reuse path (when duplicate exists)

```bash
gh issue edit <number> --repo CherryHQ/cherry-studio \
  --title "[Feature]: <new title>" \
  --body-file /tmp/req-body.md \
  --milestone "v2.1.0"
```

The original body content is overwritten — comments stay since `--body` only replaces the description.

## A worked example

**User input (raw)**:
> "我想加一个跨会话的 memory，让 AI 在不同对话间记住用户的偏好。现有 memory 只在单次会话内有效。优先级 P0，V2 之后马上做。相关 issue 我没有，你帮我看看。"

**Bilingual draft shown to user**:

```markdown
**Title (英)**: [Feature]: Cross-session Memory
**标题（中）**: 跨会话 Memory

---

### Background / 背景

**EN:**
> Cherry Studio's existing Memory feature only retains information within a single conversation. Users who switch topics or start new sessions lose context they've shared (preferences, ongoing project details, recurring facts), forcing them to re-explain themselves repeatedly.

**中:**
> Cherry Studio 现有的 Memory 只在单次会话内保留信息。用户切换话题或新建会话后，之前分享的偏好、项目细节、长期事实都会丢失，导致用户反复重述。

### Goal / 目标

**EN:**
> Users can persist memory across all conversations, so the AI naturally remembers preferences, facts, and context regardless of which topic the user is in.

**中:**
> 用户可以让记忆跨所有对话持久化，AI 在任何话题下都能记住偏好、事实、上下文。

### Spec / 具体逻辑

**EN:**
> - Users can explicitly mark information to be remembered across sessions, surfaced in the conversation when the AI commits it to long-term memory.
> - In any new conversation, the AI automatically retrieves relevant cross-session memory and incorporates it into responses.
> - Users can view, edit, and delete cross-session memory entries from a dedicated settings panel.
> - Cross-session memory persists across app restarts.

**中:**
> - 用户可以明确标记某些信息要跨会话记住，AI 写入长期记忆时在对话中明示。
> - 任何新对话里，AI 自动检索相关的跨会话记忆并融入回答。
> - 用户可在专门的设置面板查看、编辑、删除跨会话记忆条目。
> - 跨会话记忆在 app 重启后依然保留。

### Verification / 验证

**EN:**
> - In conversation A, user says "I'm a data scientist, I mainly use Python." Start conversation B and ask "recommend me learning resources" — response should target data science / Python without re-asking the user's role.
> - User toggles cross-session memory off in settings → new conversations show no retrieved memory entries and behave like a clean session.
> - Conflicting statements: in conversation A say "I use Python", later say "I use Go" — subsequent conversations should reflect the most recent statement, not both.

**中:**
> - 对话 A 里用户说"我是数据科学家，主要用 Python"。新建对话 B 问"推荐学习资源"——回答应针对数据科学/Python，不再问用户角色。
> - 用户在设置里关闭跨会话记忆 → 新对话不应检索到任何旧条目，行为如全新会话。
> - 冲突陈述：对话 A 说"我用 Python"，后来说"我用 Go"——后续对话应使用最新陈述，不应同时引用两者。

### Related / 相关

#6388 (existing single-session Memory)
```

## Notes

- This skill is for **community edition** requirements only. Enterprise requirements stay in the Feishu bitable.
- Project assignment (Project #3 fields like Status, Priority) IS done by this skill — see workflow step 7.
- If the user is creating many issues in a session, run the duplicate check once at the start by listing all open issues, then check against that list — saves repeated `gh` calls.
- Out of scope sections are NOT added by default. Only include an explicit "Out of scope" line if the user names something specific they want kept off-limits.
- **The PRD never prescribes implementation.** No file paths, no library names, no architecture choices.
- The bilingual draft is **review-only**. Only the English version is published to GitHub.
