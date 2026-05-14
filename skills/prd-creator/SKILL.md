---
name: prd-creator
description: Discuss a Cherry Studio community-edition product requirement with the user, draft a bilingual (Chinese + English) PRD for review, then — after explicit user approval — create the English-only issue on GitHub (CherryHQ/cherry-studio). Use whenever the user wants to turn a requirement (from a Feishu doc, a meeting note, a customer ask, or a rough idea) into a GitHub issue. Triggers on phrases like "create requirement doc", "create a requirement", "put this requirement on GitHub", "create new feature issue", "draft an issue for...", or anytime the user describes a Cherry Studio feature/improvement they want tracked. The format is opinionated (Background / Goal / Spec / Verification / Related, NO implementation details, draft shown bilingually for human review, issue itself written in English only).
---

# Cherry Studio Requirement Issue (PRD)

This skill helps a PM and an AI agent collaborate on a Cherry Studio requirement, draft it bilingually for review, and only then publish the English version as a GitHub issue. The issues are read by both human developers and Claude Code, so the body sticks to product logic plus concrete verification cases — **never implementation details**.

## How this skill works

The skill is a **conversation**, not a one-shot generator. The flow is:

1. **Discuss** — user describes a requirement (often roughly). Agent asks clarifying questions if needed.
2. **Research before drafting** — agent searches GitHub issues, PR history (especially closed/abandoned PRs), and repo code to ground Background in real product state — not just the items the user linked.
3. **Draft bilingually** — agent produces a draft in Chinese + English side-by-side, so the user (Chinese-speaking PM) can review fluently.
4. **Iterate with cross-section consistency** — when one section changes, agent proactively checks whether sibling sections need updating too.
5. **Validate & publish** — agent re-checks each linked issue is still relevant (drops stale/tangential links), then creates the English-only GitHub issue, adds it to Project #3, and closes any old issues fully subsumed by the new PRD with a "Tracked in #NEW" note. The Chinese gloss is review-only and does NOT enter the issue body.

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
**Title (Chinese)**: ...

---

### Background / 背景 (Background)

**EN:**
> ...

**ZH:**
> ...

### Goal / 目标 (Goal)

**EN:**
> ...

**ZH:**
> ...

### Spec / 具体逻辑 (Spec)

**EN:**
> - bullet 1
> - bullet 2

**ZH:**
> - Item 1
> - Item 2

### Verification / 验证 (Verification)

**EN:**
> - case 1

**ZH:**
> - Case 1

### Related / 相关 (Related)

#1234 #5678
```

End every draft with: **"Confirm this version goes to GitHub. Which sentence needs changing?"** (or English equivalent if the user is using English).

## Workflow

### 1. Discuss & gather input

If the user opens with a vague requirement, ask up to 3 clarifying questions before drafting. Useful questions:
- Background details: What kind of user encounters this problem in what scenario?
- Scope: Does this requirement cover X only, or Y as well?
- 关联反馈：有哪些 social feedback / GitHub issue 是这个需求的来源？(if not provided, offer to search via `gh issue list --search`)
- Priority / Milestone — these go into Project #3 fields, NOT the issue body, but record them for later.

If the user already gives enough detail — or if the requirement is concrete enough that you can pick a research keyword without asking — skip questions and go straight to step 2 (research). Don't gate research behind clarifying questions; partial research findings are often the *best* clarifying questions.

### 2. Research & ground in real product state (REQUIRED)

**Do this every time, even when the requirement looks obvious.** Three parallel searches, then synthesize before drafting. This phase is what prevents misframed Backgrounds — and surfaces related work the user didn't mention.

#### 2A. Issue search — discover related/duplicate reports

Cherry issues are bilingual, so search both languages:

```bash
gh search issues "<EN keyword>" --repo CherryHQ/cherry-studio --state all --limit 20
gh search issues "<Chinese keyword>" --repo CherryHQ/cherry-studio --state all --limit 20
```

Also check Project #3:

```bash
gh api graphql -f query='query{organization(login:"CherryHQ"){projectV2(number:3){items(first:50){nodes{content{__typename ... on Issue{number title state}}}}}}}'
```

For top candidates, read full content:

```bash
gh issue view <number> --repo CherryHQ/cherry-studio --json title,body,state,comments
```

Look for: actual user pain (not just title), workarounds users mention (they reveal the real gap), and closed issues with similar titles (often contain the proposed-but-not-shipped solution).

If a **strong duplicate** exists, recommend reusing it: "Issue #N already covers this — I suggest updating its body rather than creating a duplicate. Proceed with reuse?" Only create new if the user explicitly chooses.

#### 2B. PR history — find prior attempts

```bash
gh search prs "<keyword>" --repo CherryHQ/cherry-studio --state all --limit 20
```

For any **closed-but-not-merged** PR that looks related, read it:

```bash
gh pr view <number> --repo CherryHQ/cherry-studio --json title,body,state,closedAt,comments
```

The "why was this abandoned" answer is often the real constraint behind the new requirement. Merged PRs that touch the same area also matter — they tell you what already shipped, so Background doesn't claim "users can't do X" when X partially works.

#### 2C. Repo code — verify current product state

If you have the cherry-studio repo checked out locally, use the Grep tool. Otherwise:

```bash
gh search code "<keyword>" --repo CherryHQ/cherry-studio --limit 20
```

Look for what's actually wired up in `packages/aiCore/`, the feature area's components, and any feature flags. The point is to know the *current shape* of the product before claiming what's missing.

#### 2D. Synthesize and surface findings before drafting

After 2A+2B+2C, post a short brief to the user — do NOT skip straight to a draft:

> **Research findings before I draft:**
> - **Related open issues**: #1234 (same pain, 12 reactions), #5678 (adjacent — UI for X)
> - **Closed PR #9012** attempted this in 2024-08, abandoned because <reason from PR comments>
> - **Current state in code**: feature is gated by <flag> and only handles <case>
>
> Draft against this picture, or did I miss/misframe something?

If findings contradict the user's framing, flag it explicitly — don't paper over it:
> "I read #13625 and the agent code — the real constraint is X, not Y as we discussed. Should I draft against that?"

Concrete failure mode this prevents: the OpenAI/Anthropic interop PRD almost shipped with a generic "endpoint format mismatch" framing until research revealed the real pain was Agent mode's hard dependency on Anthropic-format endpoints — a much sharper, more actionable framing.

### 3. Draft the bilingual version

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

### 4. Self-check before showing to user

Run this checklist mentally on every draft:

- [ ] **Grounded in research**: Background and Related reflect findings from Step 2 — at least one issue/PR/code fact discovered during research, not only items the user pre-supplied. If research turned up nothing, say so explicitly rather than skipping the check.
- [ ] **No code references**: Body contains no file paths, function names, library names, or framework references. (Common offenders: `src/`, `packages/`, `.ts`, `.tsx`, `useEffect`, `Redux`, `Drizzle`.)
- [ ] **Spec ≠ Verification redundancy**: For each Verification bullet, scan the Spec list. If any Verification bullet just rephrases a Spec rule with different words, delete it. Verification should add specifics (named inputs, edge cases, negative checks) that Spec doesn't already imply.
- [ ] **Examples are current**: Provider examples use CherryIN as primary; model examples are the latest generation, not legacy.
- [ ] **No filler**: Phrases like "provide a great user experience", "improve user satisfaction", "TBD", "more details to come" — strip them.

### 5. Iterate with cross-section consistency

When the user revises one section, **proactively** check whether sibling sections need updating before re-showing the draft.

Trigger questions to ask the user when appropriate:
- Background changed → "Background now emphasizes <new framing>. Should Goal or Spec be re-aligned to match?"
- Goal narrowed → "Goal now scopes to X only. Should we drop the Y bullets from Spec / Verification?"
- A new Verification case added that contradicts existing Spec → flag it: "this Verification bullet implies Spec needs another rule. Add it?"

Don't blindly carry old sections forward when the framing shifts. The OpenAI/Anthropic interop PRD went through exactly this — Background was sharpened (Agent unlock as primary pain), and Goal/Spec/Verification all needed re-pivoting to match.

Loop until explicit confirmation ("confirm / OK / ship it / yes ship it"). Don't auto-create on a single "looks good" — wait for an unambiguous "build it" signal.

### 6. Re-validate Related links before submit

After the user has said "build it" but **before** `gh issue create` — do one last pass on the `Related` line. The list often grew across iterations, and an issue that *seemed* relevant at draft time may turn out tangential, already-fixed, or duplicated by another link on closer read.

For each `#NNNN` in Related (and any PRs on a `PRs:` line):

```bash
gh issue view <N> --repo CherryHQ/cherry-studio --json title,state,body,closedAt,stateReason
```

Check four things:

1. **Still relevant** — does the issue actually describe the same user pain, or only adjacent? If it's tangential, drop it.
2. **Not stale** — if the issue is `closed` with `stateReason: COMPLETED`, the pain it reports may already be fixed; either drop it or keep it with a note ("originally raised in #X, partially shipped, this requirement extends it").
3. **No redundancy** — two linked issues that say the same thing add noise. Pick the higher-signal one (more reactions / clearer report) and drop the other.
4. **Fully subsumed?** — if the new PRD *completely covers* the pain in an old open issue (the old issue's reporter would consider their problem fully solved by what this PRD ships), mark it as a **subsume candidate**. These get closed and pointed at the new issue in Step 8 — but only after the user confirms each one.

If any link is weak, or any look subsumable, surface it before submitting:

> "Re-checked Related:
> - #11420 still spot-on, keeping.
> - #12057 is actually about *exporting* memory, not persistence — different feature. Drop from Related?
> - #6388 and #11420 look **fully covered** by this PRD. Close them after we create the new issue, with a `Tracked in #NEW` comment? (Or keep them open if you want to preserve the discussion threads.)"

After the user confirms the final Related list **and** the subsume list, proceed to Step 7. Do **not** silently re-write Related or pre-commit to closing old issues without telling the user — they may have a reason for keeping a tangential link (e.g., a stakeholder asked for it) or for keeping an old thread open.

This step is fast (most lists are 2-4 items) and catches a common embarrassment: shipping an issue that lists `#X` as "Related" when `#X` was actually closed last week as fixed.

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

### 8. Close superseded issues (post-create housekeeping)

If Step 6 produced a confirmed **subsume list** — old issues whose pain is fully covered by the new PRD — close them now, *after* the new issue exists (so we can reference its number).

For each subsumed issue `#OLD`:

```bash
# 1. Comment on the old issue, pointing to the new one
gh issue comment <OLD> --repo CherryHQ/cherry-studio --body "Tracked in #<NEW> — the new requirement fully covers the pain reported here. Closing as superseded; please follow #<NEW> for progress, and reopen this if you feel anything is missing."

# 2. Close it as not-planned (since it's superseded, not literally completed by code)
gh issue close <OLD> --repo CherryHQ/cherry-studio --reason "not planned"
```

Notes:

- Use `--reason "not planned"` — `completed` implies code shipped, which isn't true yet at this point. `not planned` (with a clear comment) reads correctly as "we're tracking this elsewhere now".
- The comment should always be posted **before** the close, so subscribers to the old issue see context in their notifications, not just a silent close.
- The new issue's `Related` line should still list these old issue numbers — the link in both directions makes it findable from either end.
- If the user explicitly asked to keep an old thread open (e.g., active discussion), respect that and skip the close even if the PRD subsumes it. Step 6 should have already settled this.

After this step, output a one-liner:

> "Created #<NEW>, added to Project #3, closed #<OLD1> #<OLD2> as superseded."

### 9. Reuse path (when duplicate exists)

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

**Research findings posted to user before drafting** (Step 2D):

> 我搜了一下,先把背景同步给你:
> - **相关 open issues**: #6388 (现有 single-session Memory 的设计 issue)、#11420 (用户反馈:"AI 老是忘记我说过的事"，47 reactions)、#12057 (要求 export memory 的 issue,作为参考)。
> - **PR 历史**: #10832 在 2024-10 尝试过类似的 cross-session 持久化，被 close 了 — comments 里说当时 RAG pipeline 还不稳定，担心检索噪音污染回答。这个约束今天还存在吗值得留意。
> - **代码现状**: Memory 当前实现在 `packages/memory/`，只有 in-conversation context window，没有持久层；`packages/aiCore/` 里已经接好了 vector store 抽象，可以复用。
>
> 按这个画面起草,还是哪里我搞错了?

(用户确认后,进入起草。)

**Bilingual draft shown to user**:

```markdown
**Title (英)**: [Feature]: Cross-session Memory
**Title (Chinese)**: Cross-session Memory

---

### Background / 背景 (Background)

**EN:**
> Cherry Studio's existing Memory feature only retains information within a single conversation. Users who switch topics or start new sessions lose context they've shared (preferences, ongoing project details, recurring facts), forcing them to re-explain themselves repeatedly.

**ZH:**
> Cherry Studio's existing Memory only retains information within a single session. When users switch topics or start new sessions, previously shared preferences, project details, and long-term facts are lost, forcing users to repeat themselves.

### Goal / 目标 (Goal)

**EN:**
> Users can persist memory across all conversations, so the AI naturally remembers preferences, facts, and context regardless of which topic the user is in.

**ZH:**
> Users can persist memory across all conversations, so the AI remembers preferences, facts, and context regardless of topic.

### Spec / 具体逻辑 (Spec)

**EN:**
> - Users can explicitly mark information to be remembered across sessions, surfaced in the conversation when the AI commits it to long-term memory.
> - In any new conversation, the AI automatically retrieves relevant cross-session memory and incorporates it into responses.
> - Users can view, edit, and delete cross-session memory entries from a dedicated settings panel.
> - Cross-session memory persists across app restarts.

**ZH:**
> - Users can explicitly mark information to remember across sessions, with the AI indicating in conversation when it commits to long-term memory.
> - In any new conversation, the AI automatically retrieves relevant cross-session memory and incorporates it into responses.
> - Users can view, edit, and delete cross-session memory entries from a dedicated settings panel.
> - Cross-session memory persists across app restarts.

### Verification / 验证 (Verification)

**EN:**
> - In conversation A, user says "I'm a data scientist, I mainly use Python." Start conversation B and ask "recommend me learning resources" — response should target data science / Python without re-asking the user's role.
> - User toggles cross-session memory off in settings → new conversations show no retrieved memory entries and behave like a clean session.
> - Conflicting statements: in conversation A say "I use Python", later say "I use Go" — subsequent conversations should reflect the most recent statement, not both.

**ZH:**
> - In conversation A, user says "I am a data scientist, mainly use Python". New conversation B asks "recommend learning resources" — response should target data science/Python without re-asking user role.
> - User toggles cross-session memory off in settings → new conversations show no retrieved memory entries and behave like a clean session.
> - Conflicting statements: conversation A says "I use Python", later says "I use Go" — subsequent conversations should reflect the most recent statement, not both.

### Related / 相关 (Related)

#6388 (existing single-session Memory)
```

## Notes

- This skill is for **community edition** requirements only. Enterprise requirements stay in the Feishu bitable.
- Project assignment (Project #3 fields like Status, Priority) IS done by this skill — see workflow step 7.
- If the user is creating many issues in a session, run the duplicate check once at the start by listing all open issues, then check against that list — saves repeated `gh` calls.
- Out of scope sections are NOT added by default. Only include an explicit "Out of scope" line if the user names something specific they want kept off-limits.
- **The PRD never prescribes implementation.** No file paths, no library names, no architecture choices.
- The bilingual draft is **review-only**. Only the English version is published to GitHub.
