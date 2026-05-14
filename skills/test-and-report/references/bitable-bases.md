# Known Bitable Configurations

## Cherry Studio Desktop (Client) System Testing

- **base_token**: `AdeDbC9VgaNkrEsXtk5cTMarn2e`
- **Main table table_id** (Test Issues): `tbl7eUvrbfM7XFqg`
- **URL**: https://mcnnox2fhjfq.feishu.cn/base/AdeDbC9VgaNkrEsXtk5cTMarn2e
- **GitHub repo**: `CherryHQ/cherry-studio` (public)

### Field IDs

| Field | Type | ID | Notes |
|-------|------|----|-------|
| Issue Title | text | `fldNrOaPGd` | Primary field |
| Issue Description | text | `fldPLm4WIR` | Multi-line |
| Example Image | attachment | `fld7RbjUJg` | **Upload separately** |
| Module | select | `fldJnWKno4` | 17 Cherry Studio categories |
| Issue Category | select | `fldDdSGUOn` | Bug / UX Improvement |
| Priority | select | `fldNeu8G9i` | P0 / P1 / P2 |
| Status | select | `fldhPJ0Uh8` | Pending Confirmation / Confirmed / In Progress / Fixed / Verified / Deferred / Won't Fix |
| Owner | user | `fld534eZGs` | |
| Submitter | user | `fldmS8UN6v` | |
| Issue | text(url) | `fldpJVuWJR` | Value format: `[#xxx](url)` |
| Notes | text | `fldR8WITmw` | |
| Created At | created_at | `fld4kmTKsp` | System auto, read-only |

---

## Cherry Studio Enterprise (Express SaaS Staging)

- **base_token**: `IJQPbTzZhaObMQsuL5OcbaoBnag`
- **Main table table_id** (Issue Collection): `tbl20SIk4B78Ydpg`
- **URL**: https://mcnnox2fhjfq.feishu.cn/wiki/PkuVwDh42iQB3bkLGEdcndVJnuf?table=tbl20SIk4B78Ydpg
- **Staging URL**: https://cse-admin-staging.cherry-ai.com
- **GitHub repo**: `CherryInternal/cherry-studio-enterprise-api` (private, frontend in `apps/admin/`, current dev branch `saas`)

### Field IDs

| Field | Type | ID | Notes |
|-------|------|----|-------|
| Issue Title | text | `fldrugZmSN` | Primary field |
| Issue Description | text | `fldQnTONZx` | Multi-line |
| Example Image | attachment | `fldm170GcF` | **Upload separately** |
| Module | select | `fldwb6HCeQ` | Currently only "Other" placeholder, module list TBD |
| Issue Category | select | `fldcR76H92` | Bug / UX Improvement |
| Priority | select | `fldWyNzv8J` | P0 / P1 / P2 |
| Status | select | `fld2ASTnm3` | Pending Confirmation / Confirmed / In Progress / Fixed / Verified / Deferred / Won't Fix |
| Owner | user | `fldB6FJWuS` | |
| Submitter | user | `fldu4WcRMt` | |
| Issue | text(url) | `flds0thliZ` | Value format: `[#xxx](url)` |
| Notes | text | `fldvfYdQpr` | |
| Created At | created_at | `fldkJquZgQ` | System auto, read-only |

---

## View Quick Reference (Both Bases)

- **All - By Priority** (default): grid, grouped by priority
- **P0 Pending Fix**: grid, filter Priority=P0 AND Status NOT IN (Fixed/Verified/Won't Fix)
- **By Module**: grid, grouped by module
- **Status Board**: kanban, grouped by status
- **Archived**: grid, filter Status IN (Fixed/Verified/Won't Fix)

---

## If the Base Is Not in the Above List

When user's table is not in the known list:

1. First extract wiki_token or base_token from URL (`/wiki/...` needs `lark-cli wiki spaces get_node --params '{"token":"<wiki_token>"}'` to get `obj_token`)
2. `lark-cli base +table-list --base-token <token>` to find target table
3. `lark-cli base +field-list --base-token <token> --table-id <tbl>` to get field ID list and option enums
4. Dynamic adaptation: match field names, required fields inferred from "Required: Yes" in description

**Field Naming Conventions** (cross-Base consistency for fuzzy matching):
- Primary field is usually "Issue Title" or "Title"
- Single/multi-select fields use Chinese names (Issue Category / Priority / Status / Module)
- Attachment field is "Example Image" or "Screenshot" or "Attachments"
- User fields: "Submitter" / "Owner"
- URL field: "Issue" or "Issue Link"
