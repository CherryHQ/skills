# Ledger & Dashboard

User scenario for this file: after reimbursement approval is complete, generate ledger records, summary statistics, dashboard reports, or historical data analysis.

---

## Goal

Read completed reimbursement records from personal reimbursement Base (approval status "Approved" or "Paid"), generate accounting ledger, summary dashboard, and budget-vs-actual analysis.

---

## Workflow

### Phase 1 — Data Preparation

**1.1 Read Completed Records**

1. Get current user identity and corresponding personal reimbursement Base Token (see `references/feishu-base.md`)
2. Read all records from personal Base, filter where `Approval Status ∈ [Approved, Paid]`
   ```bash
   lark-cli base +record-list \
     --base-token "<personal_base_token>" \
     --table-id "<table_id>" \
     --limit 500
   ```

For global aggregation (multi-employee view), read the master Base "Reimbursement Overview" table (read-only permission).

**1.2 Filter Scope**
Filter based on user request:
- Time range (this month / this quarter / this year / custom) — filter by `Date` Unix timestamp range
- Applicant — match by user field
- Department — match by select field
- Expense type — match by select field

If user does not specify scope, default to last month summary and ask whether to expand.

---

### Phase 2 — Ledger Generation

Generate row-format records suitable for accounting entry:

```markdown
## Ledger Records

| Date | Applicant | Department | Type | Amount | Pre-tax Amount | Tax | Invoice # | Approval Status | Payment Date | Invoice Doc |
|------|-----------|------------|------|--------|---------------|------|--------|----------------|--------------|-------------|
| ...  | ...       | ...        | ...  | ...    | ...           | ...  | ...    | ...            | ...          | ...         |
```

If user requests export, generate CSV or Excel. Field mapping stays consistent with Base.

---

### Phase 3 — Summary Dashboard

Generate management-view summary reports.

**3.1 Expense Trend**
Show expense trends by time granularity (week/month):

```markdown
## Expense Trend

| Month | Total Expense | MoM |
|-------|---------------|-----|
| 2024-01 | 3200 | — |
| 2024-02 | 2800 | -12.5% |
| 2024-03 | 4500 | +60.7% |
```

> Implementation: read Base records, group by month and aggregate `Amount`. Or use `lark-cli base +data-query` for server-side aggregation.

**3.2 Category Breakdown**
Show distribution by expense type:

```markdown
## Category Distribution

| Type | Amount | Share | Count |
|------|--------|-------|-------|
| Travel | 2000 | 40% | 5 |
| Transportation | 800 | 16% | 12 |
| Entertainment | 1500 | 30% | 3 |
| ... | ... | ... | ... |
```

**3.3 Department Comparison**
If multi-department data available, show inter-department comparison:

```markdown
## Department Comparison

| Department | Total Expense | Per Capita | Largest Single |
|------------|---------------|------------|----------------|
| Engineering | 5000 | 625 | 1999 |
| Marketing | 8000 | 1000 | 3000 |
```

**3.4 Budget vs Actual**
If user provides budget data, calculate execution rate:

```markdown
## Budget Execution

| Type | Budget | Actual | Execution Rate | Status |
|------|--------|--------|----------------|--------|
| Travel | 5000 | 4200 | 84% | ✅ Normal |
| Entertainment | 3000 | 3500 | 117% | ⚠️ Over |
```

---

### Phase 4 — Anomaly Detection

Auto-flag anomalies:
- Over-budget types or departments
- Abnormally high single expenses (exceed 3× same-type average)
- Abnormal reimbursement frequency (employee密集reimbursement within short period)
- Overlong approval cycle (time from "Pending Approval" to "Approved")
- Duplicate invoice numbers (using Base "Invoice Number Duplicate Check" formula field)

---

## Base Aggregation Query (Optional)

For large data volumes, use `lark-cli base +data-query` for server-side aggregation to reduce data transfer:

```bash
lark-cli base +data-query \
  --base-token "<base_token>" \
  --json '{"type":"aggr","tableId":"<table_id>","fieldName":"Amount","aggregator":"SUM","groupBy":"Expense Type"}'
```

> Specific DSL syntax refers to Feishu Base data query documentation; adjust returned field IDs as needed.

---

## Output Formats

| Deliverable | Format | Use Case |
|-------------|--------|----------|
| Ledger | CSV / Excel | Import into accounting system |
| Dashboard | Markdown table + chart description | Management reporting |
| Anomaly Report | Markdown list | Risk control / audit |

Default inline display is Markdown. Only generate files when explicitly requested.

---

## Examples

**Example 1 — Monthly Dashboard**
Input: "Summarize this month's reimbursement, make a dashboard"
Output: Read personal Base "Approved"/"Paid" records → expense trend + category distribution + department comparison, inline Markdown tables

**Example 2 — Budget Analysis**
Input: "See Q1 budget execution, what's over"
Output: Budget vs actual table, flag over-budget items, provide anomaly analysis

**Example 3 — Ledger Export**
Input: "Export all paid reimbursements from H1 as Excel"
Output: Ledger-format Excel with Date, Applicant, Department, Type, Amount, Pre-tax Amount, Tax, Invoice #, Payment Date, etc.
