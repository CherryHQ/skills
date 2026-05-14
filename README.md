# Cherry Studio Skills

This is our team's everyday toolkit — workflows we've packaged into skills so our AI agents can handle the repetitive parts of our jobs. We use these daily for testing, product management, content creation, and operations.

We keep them public because the patterns are reusable. If you recognize your own workflow in any of these, feel free to adapt them.

---

## Why These Skills

Most of these solve a specific "coordination tax" problem: the handoff between different tools and people that eats time but doesn't require deep judgment.

| Pattern | Example | What the skill handles |
|---------|---------|----------------------|
| **Test → Track in two systems** | Find a staging bug → file in Feishu Bitable + GitHub simultaneously | Captures browser evidence, writes both records, deduplicates against existing issues |
| **Requirement → Structured PRD → Issue** | A feature idea from a meeting note → bilingual draft → GitHub issue | Enforces research (check existing issues/PRs), maintains consistent PRD format, prevents "build it" without review |
| **Transcript → Publishable content** | A recorded talk → blog post or Twitter thread | Style learning from past writing, fact-checking against sources, ASR error correction |
| **Invoice → Reimbursement → Ledger** | A stack of receipts → approval workflow → financial record | Batch aggregation, approval routing, dashboard generation |

The common thread: **humans make decisions, the skill handles the formatting, tracking, and cross-system sync.**

---

## Skill Catalog

### 🧪 Testing & Quality
| Skill | Purpose | Key Features |
|-------|---------|--------------|
| [test-and-report](skills/test-and-report/) | Manual testing + dual-track bug filing | Browser evidence capture (DOM/console/network/screenshot), simultaneous Feishu Bitable + GitHub submission, dedup enforcement, mandatory priority prompt |

### 📝 Product & Content
| Skill | Purpose | Key Features |
|-------|---------|--------------|
| [prd-creator](skills/prd-creator/) | Bilingual PRD drafting → GitHub issue | Research phase (search existing issues/PRs/code), opinionated format (Background/Goal/Spec/Verification/Related), human approval gate before creation, Project board integration |
| [transcript-to-content](skills/transcript-to-content/) | Transcripts → social posts or articles | Style learning from reference content, source fact-checking, ASR correction, multi-format output |

### 💼 Operations
| Skill | Purpose | Key Features |
|-------|---------|--------------|
| [expense-reimbursement](skills/expense-reimbursement/) | Invoice → reimbursement → ledger | Batch aggregation, approval workflow, financial dashboard |

---

## For External Contributors

These skills reference our internal infrastructure (Feishu, Cloudflare R2, specific repo addresses) because that's where we run them. The **workflow patterns** are the reusable part:

- **Dual-track submission** (test-and-report) — the idea of filing simultaneously in a project tracker and a dev tracker, with dedup
- **Approval-gated issue creation** (prd-creator) — the idea of requiring human review before an agent creates a GitHub issue
- **Style-learning content generation** (transcript-to-content) — the idea of grounding output in a corpus of past writing

If you adapt these to your own stack, we'd love to hear about it.

---

## License

[Apache 2.0](LICENSE)
