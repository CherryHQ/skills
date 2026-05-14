# Cherry Studio Skills

These are the workflows the Cherry Studio team runs every day. We package them as skills so our AI agents handle the boring stuff — browser testing, filing bugs across two systems, drafting bilingual PRDs, turning transcripts into content, processing expenses.

We're sharing the ones we've cleaned up enough to be useful outside our walls. Some of our internal skills are too tied to private tools to be worth open-sourcing, but we'll keep adding the ones that aren't.

---

## What These Solve

Most of these cut "coordination tax" — the handoffs between tools and people that burn time but don't need human judgment.

| Pattern | Example | What the skill automates |
|---------|---------|--------------------------|
| **Test → Track in two systems** | Find a staging bug → file in Feishu Bitable + GitHub simultaneously | Captures browser evidence (DOM, console, network, screenshots), writes both records, deduplicates against existing issues |
| **Requirement → Structured PRD → Issue** | A feature idea from a meeting note → bilingual draft → GitHub issue | Enforces research (search existing issues, PRs, code), locks format (Background/Goal/Spec/Verification/Related), requires human approval before creation |
| **Transcript → Publishable content** | A recorded talk → blog post or thread | Learns style from past writing, fact-checks against sources, corrects ASR errors |
| **Invoice → Reimbursement → Ledger** | A stack of receipts → approval workflow → financial record | Batch aggregation, approval routing, dashboard |

The pattern: **humans decide, the skill formats, tracks, and syncs across systems.**

---

## Skills

### 🧪 Testing & Quality
| Skill | Purpose | What it does |
|-------|---------|--------------|
| [test-and-report](skills/test-and-report/) | Manual testing + dual-track bug filing | Captures browser evidence, files simultaneously to Feishu Bitable and GitHub, enforces dedup, prompts for priority |

### 📝 Product & Content
| Skill | Purpose | What it does |
|-------|---------|--------------|
| [prd-creator](skills/prd-creator/) | Bilingual PRD → GitHub issue | Research phase, opinionated format, human approval gate, Project board integration |
| [transcript-to-content](skills/transcript-to-content/) | Transcripts → posts or articles | Style learning, source fact-checking, ASR correction, multi-format output |

### 💼 Operations
| Skill | Purpose | What it does |
|-------|---------|--------------|
| [expense-reimbursement](skills/expense-reimbursement/) | Invoice → reimbursement → ledger | Batch aggregation, approval workflow, financial dashboard |

---

## For External Use

These skills reference our internal stack (Feishu, Cloudflare R2, specific repos) because that's where we run them. The **workflow patterns** are what's reusable:

- **Dual-track submission** — filing simultaneously in a project tracker and a dev tracker, with dedup
- **Approval-gated issue creation** — requiring human review before an agent creates a GitHub issue
- **Style-grounded content generation** — grounding output in a corpus of past writing

Adapt them to your stack. More skills coming.

---

## License

[Apache 2.0](LICENSE)
