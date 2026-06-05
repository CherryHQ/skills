# Patch Schema — V1 Reference

## Complete patches.json Schema

```json
{
  "patch_version": "1.1",
  "source_file": "/path/to/original.docx",
  "generated_at": "2026-02-27T10:35:00Z",
  "output_strategy": "SAFE",
  "patches": [
    {
      "patch_id": "p001",
      "type": "replace_text",
      "target_para_id": "sec_1_p2",
      "original_text": "Developed dashboards using Tableau",
      "match_mode": "contains",
      "occurrence_index": 0,
      "replacement_text": "Built 3 Tableau dashboards (⚠️ Estimate) tracking weekly KPIs for a 10-person analytics team, reducing ad-hoc reporting requests by ~30%",
      "comment": "【JD对齐】JD 3次提及 'data visualization' 和 'dashboard'. 原句缺少数量和影响. 改写遵循 Action+Method+Tool+Result 框架. ⚠️ Estimate: 数量3和团队规模10基于用户在Q&A中的估算, 需在提交前确认.",
      "comment_author": "Resume Optimizer AI",
      "comment_initials": "RO",
      "quant_label": "ESTIMATE",
      "jd_requirement_ref": "Req#2: Data visualization proficiency (Tableau mentioned 3x)",
      "dimension": "keyword"
    },
    {
      "patch_id": "p002",
      "type": "comment_only",
      "target_para_id": "sec_1_p4",
      "comment": "❓ Need confirm: 如果你可以回忆该项目处理的数据量 (行数/GB/样本量), 在此处补充会显著增强可信度. 示例: 'Processed ~50K customer records' 或 'Analyzed 2GB of transaction logs'",
      "comment_author": "Resume Optimizer AI",
      "comment_initials": "RO",
      "quant_label": "NEED_CONFIRM",
      "jd_requirement_ref": "Req#4: Experience with large-scale data",
      "dimension": "impact"
    }
  ],
  "stats": {
    "total_patches": 2,
    "replace_text": 1,
    "comment_only": 1,
    "dimensions_touched": ["keyword", "impact"]
  }
}
```

---

## Patch Types (V1)

### `replace_text`

Replace the **entire paragraph** identified by `target_para_id`. Always add a comment.

**When to use:**
- JD keyword not present → add keyword to an existing relevant bullet
- Weak/passive verb → replace with action verb
- Activity-based bullet → reframe with quantification (Fact or confirmed Estimate only)
- ATS fix → convert table cell content to regular paragraph text

**Critical constraints:**
- `original_text` must exist within the target paragraph (verified using `match_mode`)
- The `replacement_text` replaces the ENTIRE paragraph text (not just the matched portion)
- If `original_text` is not matched, write_resume.py will apply a comment-only fallback
- NEVER use `replace_text` for `NEED_CONFIRM` items

### `comment_only`

Add a Word comment to the paragraph without any text change.

**When to use:**
- `NEED_CONFIRM` items where user data is insufficient
- Suggestions that require human judgment (e.g., verify a number before submitting)
- ATS warnings (flagging table content that should be reviewed)
- Informational notes about why a section is strong

---

## match_mode Values

| mode | Behavior | Use when |
|------|----------|----------|
| `exact` | `normalize(original_text) == normalize(paragraph_full_text)` | You want to match the entire paragraph exactly |
| `contains` (default) | `normalize(original_text) in normalize(paragraph_full_text)` | Most cases — a distinctive phrase within the paragraph |
| `fuzzy` | After normalization, checks substring with tolerance for punctuation/whitespace | When you're unsure about exact whitespace or unicode in the source |

**Recommendation:** Always use `contains` (default) unless you have a specific reason. Use `exact` only when the paragraph is very short and you want strict matching.

---

## occurrence_index

When multiple paragraphs match the `original_text` (rare but possible), `occurrence_index` specifies which one to use:
- `0` = first match (default)
- `1` = second match
- etc.

For most cases, the `para_id` (from parse_resume.py output) is the primary identifier and `original_text` is a consistency check. If `para_id` is correctly specified, occurrence_index is rarely needed.

---

## Quantification Labels

Every patch MUST have a `quant_label`. This drives both the comment content and the SAFE/BOOSTED decision:

| Label | Body Text | Comment | When to Use |
|-------|-----------|---------|-------------|
| `FACT` | ✅ Write into body | Note that it's confirmed | User explicitly confirmed the number |
| `ESTIMATE` | SAFE: comment only / BOOSTED: body after user confirms | `⚠️ Estimate: [reasoning]` | Reasonable inference, user-confirmed in BOOSTED mode |
| `NEED_CONFIRM` | NEVER in body | `❓ Need confirm: [what to verify]` | Insufficient info; user declined to confirm |
| `null` | N/A | Describe the change (no quant label needed) | Non-quantification changes (verb replacement, keyword addition) |

---

## Comment Writing Guide

Every comment must contain:

1. **JD alignment:** Which JD requirement this change addresses (use `jd_requirement_ref`)
2. **Why this improves fit:** In 1-2 sentences, explain the reasoning
3. **Quantification label** (if applicable): Fact ✅ / Estimate ⚠️ (with basis) / Need confirm ❓

**Comment language:** Chinese preferred for user readability. Technical terms can be in English with Chinese parenthetical.

**Good comment example:**
```
【JD对齐 Req#3: A/B testing (4次提及)】原文未提及任何实验设计。
将项目描述重构为包含实验对比框架。✅ Fact: 用户确认曾对比两种推荐算法。
Action verb 'Designed' 替换被动结构以提升专业度。
```

**Bad comment example:**
```
Changed the wording to sound better.
```

---

## normalize_text Consistency

The `original_text` in each patch will be matched against the `full_text` field from parse_resume.py. Both use the same `normalize_text()` function from `text_utils.py`.

When writing `original_text`, use the `full_text` value from the parsed JSON (not the `raw_text`). This ensures matching works correctly even when the source document has non-breaking spaces, smart quotes, or zero-width characters.

---

## Iron Rules (Summary)

1. NEVER write `replace_text` for `NEED_CONFIRM` items
2. NEVER invent companies, project names, awards, dates, or titles
3. Every `replace_text` patch must have `original_text` that appears in the target paragraph
4. Every patch (both types) must have a non-empty `comment`
5. Every patch must have `jd_requirement_ref` linking it to a specific JD requirement
6. In SAFE mode, `quant_label: "ESTIMATE"` → automatically use `comment_only`
7. In BOOSTED mode, `quant_label: "ESTIMATE"` → use `replace_text` only after explicit user confirmation in Phase 4
