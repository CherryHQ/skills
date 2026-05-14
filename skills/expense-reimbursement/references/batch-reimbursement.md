# Batch Reimbursement (Aggregation + Draft + Approval)

User scenario for this file: batch aggregate staged invoices, generate reimbursement draft, perform validation, initiate approval workflow.

> Connects with the "Invoice Intake" phase: intake records status as "Pending Approval", batch phase advances them into the approval workflow.

---

## Goal

Read all "Pending Approval" records from the personal reimbursement Base, group and categorize them, perform full rule validation, generate a reimbursement draft for employee confirmation, then package it for manager review and finance approval.

---

## Workflow

### Phase 1 — Aggregation & Categorization

**1.1 Read Pending Records**

1. Get current user identity: `lark-cli api GET "/open-apis/authen/v1/user_info"`
2. Locate personal reimbursement Base Token from the master index (see `references/feishu-base.md`)
3. Read all records from personal Base, filter where `Approval Status = Pending Approval`
   ```bash
   lark-cli base +record-list \
     --base-token "<personal_base_token>" \
     --table-id "<table_id>" \
     --limit 200
   ```

If user provides external files (Excel/CSV), read and merge them too.

**1.2 Group by Type**
Group by expense type (Travel / Dining / Transportation / Office Supplies / Communications / Training / Entertainment / Other).

**1.3 Time Range Inference**
Infer reimbursement period from earliest to latest record date. If span exceeds one calendar month, ask user whether to split into multiple months.

---

### Phase 2 — Rule Validation

Perform the following checks on all records:

| Check | Validation Content |
|-------|-------------------|
| **Duplicate reimbursement** | Invoice number duplicates across all personal Base records (using "Invoice Number Duplicate Check" formula field or local comparison) |
| **Completeness** | Required fields missing (Date, Amount, Type, Description) |
| **Amount合理性** | Single item amount abnormally high (exceeds 3× same-type average) |

Generate a **validation report**, listing each issue with severity (⚠️ Warning / ❌ Blocker) and explanation.

---

### Phase 3 — Draft Generation

**3.1 Generate Reimbursement Draft**
Aggregate all validated items into a reimbursement application draft:

```markdown
# Reimbursement Draft — [Applicant] — [Date Range]

## Basic Info
- Applicant: [Name]
- Department: [Dept]
- Application Date: YYYY-MM-DD
- Reimbursement Period: YYYY-MM-DD ~ YYYY-MM-DD

## Expense Details
| # | Date | Type | Description | Merchant | Amount | Pre-tax Amount | Tax | Invoice # | Invoice Doc |
|---|------|------|-------------|------|--------|---------------|------|--------|-------------|
| 1 | ...  | ...  | ...         | ...  | ...    | ...           | ...  | ...    | ...         |

## Category Summary
| Type | Amount | Share |
|------|--------|-------|
| Travel | 553 | 35% |
| ... | ... | ... |
| **Total** | **1200** | **100%** |

## Validation Results
- ✅ / ⚠️ / ❌  [list each]

## Items to Confirm
- [ ] 2024-03-02 Travel: invoice number missing
```

**3.2 Employee Confirmation**
Present draft, ask employee to:
- Confirm or correct any field
- Supplement missing description / project / attachments
- Accept or reject validation flags

If employee rejects, record corrections, return to Phase 1 for reprocessing.

---

### Phase 4 — Approval Workflow

**4.1 Generate Approval Package**
After employee confirmation, generate **approval package**:
- Expense detail table
- Validation report
- Category summary
- Supporting attachment index (extracted from Base attachment fields)

**4.2 Manager Review**
Present in format suitable for direct manager quick decision:
- Total amount
- Largest single expense
- Flagged items list
- Budget impact summary

**4.3 Finance Review**
After manager approval, present **finance review package**:
- Compliance (invoice completeness, authenticity)
- Budget execution status
- Cost center allocation

**4.4 Rejection Handling**
If rejected at any stage, record:
- Rejection reason
- Required corrections
- Return to employee for modification and resubmission
- Update corresponding records in personal Base to `"Rejected"`

---

### Phase 5 — Status Update (Base Write)

After approval workflow completes, batch-update approval status of corresponding records in personal Base.

**5.1 Batch Status Update**

```bash
lark-cli api POST "/open-apis/bitable/v1/apps/<base_token>/tables/<table_id>/records/batch_update" \
  --data '{
    "records": [
      {"record_id":"rec_xxx","fields":{"Approval Status":"Approved"}},
      {"record_id":"rec_yyy","fields":{"Approval Status":"Approved"}}
    ]
  }'
```

Status flow:
- Manager approved → `"Approved"`
- Finance paid → `"Paid"` + update `Payment Date`
- Rejected → `"Rejected"` (return to employee for modification)

**5.2 Payment Date Write**
After payment completes, update `Payment Date` field to current date (Unix timestamp in seconds).

```bash
TS=$(date +%s)
lark-cli api PATCH "/open-apis/bitable/v1/apps/<base_token>/tables/<table_id>/records/<record_id>" \
  --data "{\"fields\":{\"Approval Status\":\"Paid\",\"Payment Date\":$TS}}"
```

---

## Output Formats

| Deliverable | Format | Use Case |
|-------------|--------|----------|
| Reimbursement Draft | Markdown table | Inline confirmation with employee |
| Approval Package | Markdown table + bullet summary | Manager review |
| Finance Review Table | Markdown table + flags | Finance compliance check |

Default inline display is Markdown. Only generate files when explicitly requested.

---

## Examples

**Example 1 — End-of-month batch reimbursement**
Input: "Help me organize this month's reimbursement, those invoices I entered before"
Output: Read personal Base "Pending Approval" records → aggregate by category → validate → generate draft → employee confirm → approval package

**Example 2 — Travel batch reimbursement**
Input: "Submit those invoices from the business trip together: train, hotel, client dinner"
Output: Group by Travel / Dining / Entertainment, generate complete draft, flag same-day Travel+Dining reasonableness

**Example 3 — Rejection correction**
Input: "Manager said entertainment expense was over limit, help me fix and resubmit"
Output: Locate over-limit entertainment, propose split-order or cost-center adjustment options, fix in personal Base, change status back to "Pending Approval" for resubmission
