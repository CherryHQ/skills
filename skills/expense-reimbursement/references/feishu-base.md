# Feishu Bitable Reference (Base / Bitable)

> Reference lookup: auth check, config constants, field schema. All Base write operations go through `scripts/invoice_intake.py` — do not manually construct lark-cli commands.

---

## Prerequisites

Before any Feishu table operation, confirm OAuth is connected:

```bash
lark-cli auth status
```

If not connected:

```bash
lark-cli auth login --domain base,drive,sheets,contact
```

---

## Config

| Config Item | Value |
|-------------|-------|
| Master Index Base Token | `JGzKb5SKSal9A3suMyRcxRepnLe` |
| Master Index Table ID | `tblavWeOwUGHQZhA` |

> The master table stores "Name → Personal Reimbursement Base Token" mapping. Read-only, no writes.

---

## Personal Reimbursement Table Field Schema

Fields are determined by actual table structure. Dynamically fetch via:

```bash
# First locate personal Base token (match by name from master index)
lark-cli base +field-list \
  --base-token "<personal_base_token>" \
  --table-id "<table_id>"
```

---

## Key Gotchas

| Gotcha | Description |
|--------|-------------|
| Date format | datetime fields accept **millisecond-level** Unix timestamp (seconds × 1000). Passing seconds shows 1970. |
| Attachment path | `+record-upload-attachment --file` only accepts relative paths. Must `cd` to the file directory first. |
| Advanced permissions | When Base has advanced permissions enabled, app/user needs edit permission or gets `91403 Forbidden`. |
| Select fields | Pass option name string, case-sensitive, must match Base config exactly. |
| Formula / auto_number | Read-only, skip during writes. |
