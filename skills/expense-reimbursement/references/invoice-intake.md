# Invoice Intake (Single Submission — Staging)

User scenario: enter one or multiple invoices for staging, do not immediately generate a reimbursement application.

---

## Workflow

### 1. Read Input

Supports: images (photo/screenshot), PDF (e-invoice/scan), text (dictated or pasted).

If user provides no content, ask: "Please upload an invoice image or PDF, or tell me the invoice information."

### 2. Parse & Extract

Extract from invoice:

| Field | Description |
|-------|-------------|
| Invoice Number | Required |
| Date | Required, YYYY-MM-DD |
| Amount | Required, total including tax |
| Pre-tax Amount | Required |
| Tax | Optional, default 0 if missing |
| Expense Type | Required, see type mapping below |
| Description | Required, short description |
| Attachment Path | Invoice file local path |

**Type Mapping:** Restaurant/delivery → Dining (internal) or Entertainment (client); train/plane → Travel; taxi/subway → Transportation.

### 3. Validation

| Check | Handling Strategy |
|-------|------------------|
| **Required missing** | Date/Amount unrecognizable → ❌ Ask user to supplement |
| **Non-critical missing** | Tax missing / type ambiguous → ⚠️ AI infers and continues, note in summary |

> Duplicate invoice check is handled by script (exit code 2), AI does not need to pre-query Base.

### 4. Call Script to Write

```bash
cd <invoice-file-directory>
uv run <skill_path>/scripts/invoice_intake.py \
  --invoice-number "<invoice-number>" \
  --invoice-date "<YYYY-MM-DD>" \
  --amount <total-amount> \
  --pretax-amount <pre-tax-amount> \
  --tax <tax> \
  --expense-type "<expense-type>" \
  --description "<description>" \
  --file "./<filename>"
```

Script handles: user identity, Base location, timestamp conversion, dedup, record write, attachment upload.

**Exit codes:**
- `0` — Success, stdout outputs JSON (includes `record_id`)
- `2` — Duplicate invoice number, inform user and ask whether to overwrite

### 5. Report Result

```
✅ Entered and saved to personal reimbursement table

| Invoice # | Merchant | Amount | Pre-tax Amount | Tax | Type | Status |
|-----------|----------|--------|---------------|------|------|--------|
| 261... | Beijing Daojiu... | ¥94.00 | ¥93.07 | ¥0.93 | Dining | Pending Approval |

Attachment: uploaded to "Invoice Document" field

To organize reimbursement, say "help me reimburse".
```
