# Test Case 2: 社招流程 — Analytics Manager 量化缺失

## Setup

**JD:** `mock_jd_社招.txt` (ByteDance Senior Data Analytics Manager)
**Resume:** Mock structure with 5 years experience, all activity-based bullets

### Mock Resume Structure

```
李大鹏
Email: dapeng@example.com | Phone: 139-0000-0000
LinkedIn: linkedin.com/in/dapeng

EXPERIENCE

Senior Data Analyst | XYZ E-commerce | Mar 2022 – Present
• Managed a team of analysts for the Growth division
• Built dashboards for weekly business review
• Worked with product managers to design experiments
• Led a project to improve user retention

Data Analyst | ABC Tech | Jun 2020 – Feb 2022
• Was responsible for the analytics for user acquisition campaigns
• Helped stakeholders understand data insights
• Worked on data pipeline improvements
• Collaborated with cross-functional teams

EDUCATION
Peking University — B.S. Statistics | 2016 – 2020

SKILLS
Python, SQL, Tableau, R, Hive, Spark
```

## Expected Behavior

### Phase 3: Diagnose (Expected Scores ~社招 weights)
- Dimension 1 (Eligibility): ~85 — 4 years experience vs 5+ required, slight risk
- Dimension 2 (Keyword): ~65 — Python ✅, SQL ✅, Tableau ✅, A/B testing ❌ (JD requires), causal inference ❌
- Dimension 3 (Impact): ~15 — 12 bullets, ZERO numbers
- Dimension 4 (Competency): ~60 — management ⚠️ (mentioned but no evidence), A/B ❌
- Dimension 5 (Story): ~70 — clear timeline
- Dimension 6 (Language): ~40 — "was responsible for" (×2), "helped" (×1), "worked on" (×2)
- Dimension 7 (ATS): ~85 — no tables detected, clean formatting

### Phase 4: Gap Q&A (Expected Questions ~8)
1. Team size at XYZ? (JD requires 2+ years people management)
2. Dashboard users/stakeholders count? How many dashboards built?
3. Experiment scale: how many A/B tests designed? What lift was observed?
4. User retention project: what was the baseline retention rate? What improved?
5. User acquisition analytics: what was the campaign budget or scale?
6. Pipeline improvements: what was the impact (latency reduction? data freshness?)
7. Years of SQL experience? (JD requires "expert-level")
8. Spark/Hive usage: project scale, data volume?

### Expected Patches
- 8+ `replace_text` patches (quantification + verb replacements)
- 3 `comment_only` patches (for 3 declined quantification questions)
- Weak verb replacements:
  - "was responsible for" → "Owned" (×2)
  - "helped stakeholders understand" → "Synthesized data insights for 5+ stakeholder teams" (with Q&A)
  - "worked on" → appropriate action verb

### Pass Criteria
✅ 3 declined quantifications → `comment_only` patches, NOT body text
✅ Impact dimension shows score improvement path in diagnosis
✅ All weak verb replacements have Word comments with JD_requirement_ref
✅ A/B testing gap creates a specific Q&A question
✅ Management dimension flagged properly (evidence exists but not quantified)
✅ 6+ interview follow-up questions, Impact group has quantity-specific questions
