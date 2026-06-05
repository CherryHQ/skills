# Diagnostic Rubric — 7-Dimension Scoring Guide

## Output Template

Use this exact Markdown structure for every diagnostic report. Do not omit any dimension.

---

```markdown
# 简历诊断报告

**目标职位：** [target_role_title]
**目标公司：** [target_company]
**岗位方向：** [target_track]
**招聘类型：** [mode]
**诊断时间：** [YYYY-MM-DD HH:MM UTC]
**总分：** [weighted_total]/100

> ℹ️ Eligibility信号不作为淘汰依据，仅为风险提示。优化流程照常进行。

---

## 得分总览

| # | 维度 | 得分 | 权重（校招/社招）|
|---|------|------|-----------------|
| 1 | Eligibility & Risk Signals | [0-100] | 10% / 15% |
| 2 | Keyword + Evidence | [0-100] | 25% / 20% |
| 3 | Impact & Quantification | [0-100] | 20% / 25% |
| 4 | Competency Map | [0-100] | 20% / 15% |
| 5 | Story & Structure | [0-100] | 15% / 10% |
| 6 | Language & Trust | [0-100] | 5% / 10% |
| 7 | ATS & Formatting | [0-100] | 5% / 5% |
| **加权总分** | | **[total]** | |

---

## Dimension 1: Eligibility & Risk Signals（资格与风险信号）

**得分：** [0-100] | **权重：** 10%（校招）/ 15%（社招）
⚠️ **此维度永不阻断流程。以下为风险提示，不作淘汰依据。**

### 资格检查

| JD要求 | 简历状态 | 差距说明 |
|--------|----------|----------|
| [req]  | ✅ 满足 / ⚠️ 部分满足 / ❌ 不满足 | [gap] |

### 风险标志
- [risk flag 1]

### 缓解方案（使用现有经历弥补）
- [mitigation using courses / projects / internships]

### 建议在 Gap Q&A 中确认
- [any critical missing info to ask in Phase 4]

---

## Dimension 2: Keyword + Evidence（关键词覆盖与证据链）

**得分：** [0-100] | **权重：** 25%（校招）/ 20%（社招）
**覆盖率：** [X]%（[covered] / [total] 个关键词）

### 关键词映射

| JD 关键词 | 频率 | 简历证据 (para_id) | 状态 |
|----------|------|-------------------|------|
| [kw]     | [n]x | sec_N_pM: "[excerpt]" | ✅ COVERED |
| [kw]     | [n]x | — | ❌ GAP → g001 |
| [kw]     | [n]x | sec_N_pM: "[excerpt]" | ⚠️ PARTIAL |

### 关键问题
- [issue]

### 修复建议
- [fix — map to specific patch]

---

## Dimension 3: Impact & Quantification（影响力与量化）

**得分：** [0-100] | **权重：** 20%（校招）/ 25%（社招）

### Bullet 量化分析

| para_id | Bullet 摘要 | 当前状态 | 建议 |
|---------|------------|----------|------|
| sec_N_pM | "[text]" | ❌ 无数字 | 需在Q&A中确认数据规模 |
| sec_N_pM | "[text]" | ✅ 已量化 | — |

### 主要问题
- [issue]

### 修复建议（校招友好）
- [fix with alternative quantification template if applicable]

---

## Dimension 4: Competency Map（能力结构）

**得分：** [0-100] | **权重：** 20%（校招）/ 15%（社招）

### JD 能力链 vs 简历覆盖

| JD 核心能力 | 简历覆盖度 | 关键证据 |
|------------|-----------|----------|
| [skill]    | ✅ 充分 / ⚠️ 薄弱 / ❌ 缺失 | [evidence or gap] |

### 主要问题
- [issue]

### 修复建议
- [fix]

---

## Dimension 5: Story & Structure（叙事与逻辑）

**得分：** [0-100] | **权重：** 15%（校招）/ 10%（社招）

### 时间线检查
- 时间顺序：[consistent / 存在跳跃: YYYY.MM → YYYY.MM 断层]
- 经历完整性：[assessment]

### 主要问题
- [issue]

### 修复建议
- [fix]

---

## Dimension 6: Language & Trust（语言专业度与可信度）

**得分：** [0-100] | **权重：** 5%（校招）/ 10%（社招）

### 弱动词检测

| para_id | 当前用词 | 建议替换 |
|---------|---------|---------|
| sec_N_pM | "was responsible for" | "Owned" |
| sec_N_pM | "helped with" | "Contributed to" |

### 空话/水词检测
- [detected fluff phrases]

### 主要问题
- [issue]

### 修复建议
- [fix]

---

## Dimension 7: ATS & Formatting（ATS 友好度）

**得分：** [0-100] | **权重：** 5%（校招 + 社招）

### ATS 检查项

| 检查项 | 状态 | 建议 |
|--------|------|------|
| 表格内容 | [has_tables: ✅正常 / ⚠️ 检测到表格] | 建议转为纯文本段落 |
| 文本框 | [textboxes_possible: ✅ / ⚠️ 可能存在（best-effort）] | ATS 通常跳过文本框内容 |
| 多栏布局 | [multi_column_possible: ✅ / ⚠️ 可能存在（best-effort）] | ATS 可能误读栏顺序 |
| 日期格式 | [formats found] | 建议统一为 "Mon YYYY"（如 "Jun 2025"）|
| 标题层级 | [consistent / 不一致] | 建议使用 Word 内置标题样式 |

### 主要问题
- [issue]

### 修复建议
- [fix]

---

## JD → 简历证据映射（完整表）

| JD 要求 | 类型 | 简历证据 (para_id) | 状态 |
|---------|------|-------------------|------|
| [req]   | 硬技能 | sec_N_pM: "[excerpt]" | ✅ COVERED |
| [req]   | 方法论 | — | ❌ GAP → g001 |
| [req]   | 软技能 | sec_N_pM: "[excerpt]" | ⚠️ PARTIAL |
```

---

## Scoring Guidelines

### Dimension 1 — Eligibility & Risk Signals
- 90-100: All hard requirements met
- 70-89: Minor mismatches (e.g., major adjacent but not exact)
- 50-69: Notable gap (e.g., graduation year earlier/later than range)
- 30-49: Significant mismatch (e.g., unrelated major, missing required certification)
- 0-29: Critical gap (e.g., visa/location requirement cannot be met)

**Always include mitigation strategies regardless of score. Score 0 does NOT stop the workflow.**

### Dimension 2 — Keyword + Evidence
- 90-100: ≥ 85% keywords covered with strong evidence
- 70-89: 70-84% covered
- 50-69: 50-69% covered
- 30-49: 30-49% covered
- 0-29: < 30% covered

**Evidence = a specific resume bullet or sentence that demonstrates the keyword in practice, not just listing the keyword in a skills section.**

### Dimension 3 — Impact & Quantification
- 90-100: ≥ 80% of bullets have numbers or clearly labeled estimates
- 70-89: 60-79% quantified
- 50-69: 40-59% quantified
- 30-49: 20-39% quantified
- 0-29: < 20% quantified or all activity-based

**校招 note:** Academic project metrics count. Estimate ⚠️ with user confirmation counts as quantified.

### Dimension 4 — Competency Map
- Identify the JD's core skill chain (typically 4-6 competencies for the role)
- Each competency that is COVERED by at least one strong evidence item: +20 points (for 5-item chain)
- PARTIAL (mentioned but no strong evidence): +10
- MISSING: 0

### Dimension 5 — Story & Structure
- Timeline gaps of > 3 months with no explanation: -10 per gap
- Inconsistent date formats: -5
- Role descriptions contradicting each other: -15
- Clear narrative progression (each role builds on previous): +20

### Dimension 6 — Language & Trust
- Passive verb count > 3: -15
- Vague phrases ("hardworking", "passionate about", "responsible for"): -10 each, max -30
- Action verb rate > 80%: +20
- Method-Result structure in most bullets: +20

### Dimension 7 — ATS & Formatting
- Tables detected: -20 (warn)
- Textboxes possible: -15 (warn, best-effort)
- Date format inconsistency: -10
- Multi-column possible: -15 (warn, best-effort)
- Uses Word heading styles correctly: +20
