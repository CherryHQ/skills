---
name: expense-reimbursement
description: Full lifecycle expense reimbursement: single invoice intake and staging, batch aggregation to generate reimbursement drafts, approval workflow, ledger and dashboard. Trigger when user mentions reimbursement, expenses, invoices, travel reimbursement, approval workflow, or needs to organize / verify / approve expense records. Also applies when user needs to enter invoices, view reimbursement dashboards, ledgers, or compliance checks.
---

# Expense Reimbursement

## Overview

```
Single invoice intake (staging) → Batch aggregation (draft + approval) → Ledger & Dashboard (reports)
```

## Interaction Principles

- **Default to execute, ask only on error**: after receiving an invoice, auto-complete parsing, writing, and uploading. Only interrupt if critical fields are missing or config is missing.
- **Results-oriented**: after completion, show a "saved" summary directly. No intermediate "pending confirmation" states.
- **Config-first**: use the Base token already configured in reference files. Do not ask user for it repeatedly.

---

## Built-in Scripts

All invoice intake Base operations are handled by `scripts/invoice_intake.py`. **Do not manually construct lark-cli commands.**

- **AI handles:** parsing invoice, determining expense type, generating reason description
- **Script handles:** user identity, Base location, timestamp conversion, dedup, writing, attachment upload

See `references/invoice-intake.md` Step 4 for details.

---

## Routing Rules

| User Scenario | Read File |
|---------------|-----------|
| Submit an invoice, stage it first | `references/invoice-intake.md` |
| End-of-month batch aggregation, generate reimbursement draft, initiate approval | `references/batch-reimbursement.md` |
| View ledger, summary reports, budget analysis | `references/ledger-dashboard.md` |

When intent is unclear, ask: "Do you want to stage an invoice first, or organize and submit a reimbursement form for approval now?"
