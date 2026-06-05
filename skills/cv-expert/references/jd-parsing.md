# JD Parsing Strategy

## Section Priority Order

When extracting keywords and requirements from a JD, process sections in this priority order:

1. **Must extract from:** Responsibilities / Job Responsibilities / What You'll Do / 职责 / 工作内容
2. **Must extract from:** Requirements / Qualifications / What We're Looking For / 要求 / 任职资格 / 基本要求
3. **Must extract from:** Preferred / Nice-to-have / Bonus / 加分项 / 优先条件
4. **SKIP entirely for keyword extraction:** Benefits / Perks / Why Join Us / Culture / About Us / About the Team / Equal Opportunity / Compensation / 福利 / 公司介绍

**If no section headers are present:** treat the entire JD as a flat document and extract all requirement-like sentences. Flag low confidence (see below).

---

## Extraction Schema

For each JD, produce this structure (internal, not shown to user):

```json
{
  "must_have": [
    { "text": "Bachelor's degree in CS or related field", "type": "degree", "keywords": ["Bachelor's", "CS"] },
    { "text": "2+ years Python experience", "type": "years_exp", "keywords": ["Python"] },
    { "text": "Proficient in SQL", "type": "hard_skill", "keywords": ["SQL"] }
  ],
  "preferred": [
    { "text": "Experience with Spark or distributed systems", "type": "hard_skill", "keywords": ["Spark", "distributed systems"] }
  ],
  "responsibilities": [
    "Build and maintain data pipelines",
    "Collaborate with cross-functional teams to define metrics"
  ],
  "keywords": [
    { "word": "Python", "frequency": 5, "priority": "HIGH", "category": "hard_skill" },
    { "word": "SQL", "frequency": 3, "priority": "HIGH", "category": "hard_skill" },
    { "word": "Tableau", "frequency": 2, "priority": "MEDIUM", "category": "hard_skill" },
    { "word": "A/B testing", "frequency": 1, "priority": "LOW", "category": "methodology" },
    { "word": "stakeholder", "frequency": 4, "priority": "HIGH", "category": "soft_skill" }
  ],
  "jd_type": "校招",
  "confidence": "HIGH"
}
```

---

## Keyword Extraction Rules

### Frequency-Based Priority
- **HIGH:** appears ≥ 3 times in the JD
- **MEDIUM:** appears 2 times
- **LOW:** appears 1 time

### Synonym Handling
Expand each keyword to include common synonyms/variations. Treat any as a match:
- "ML" = "Machine Learning" = "机器学习"
- "NLP" = "Natural Language Processing"
- "BA" = "Business Analytics" = "Business Analysis"
- "Python" = "Python3" = "Python programming"
- "visualization" = "data visualization" = "dashboard"

### Category Labels
- `hard_skill`: Programming languages, tools, frameworks, platforms (Python, SQL, Tableau, AWS)
- `methodology`: Processes and approaches (A/B testing, Agile, CRISP-DM, hypothesis testing)
- `domain`: Business domains (fintech, e-commerce, supply chain, healthcare)
- `soft_skill`: Interpersonal and communication (stakeholder management, collaboration, leadership)
- `degree`: Education requirements
- `years_exp`: Experience duration requirements

### Multi-Word Phrase Handling
Always extract multi-word technical phrases as a single unit:
- "machine learning" (not "machine" + "learning")
- "A/B testing" (not "A/B" + "testing")
- "data pipeline" (not "data" + "pipeline")
- "cross-functional teams" (not "cross-functional" + "teams")

---

## 校招 JD Recognition Rules

Flag the JD as 校招 type when you detect:
- "应届" / "应届毕业生" / "fresh graduate" / "new grad"
- "实习" / "intern" / "internship"
- "0-1 年" / "0 to 1 year" / "entry level" / "no experience required"
- Graduation year window within next 2 years (e.g., "Class of 2025/2026")
- "GPA" mentioned as a requirement

In 校招 mode, hard requirements like "3+ years of experience" should be noted as a risk signal (Dimension 1), not treated as a blocker.

---

## Low Confidence Detection

Mark extraction confidence as LOW when:
- No section headers found in the JD
- Total extracted Must-have items < 5
- Total unique keywords (excluding stop words) < 10
- JD text < 200 characters

When confidence is LOW:
- Include a note in the diagnostic report: "⚠️ JD 结构不清晰，关键词提取置信度较低。建议提供更完整的JD以提升诊断精度。"
- Cap Keyword Coverage dimension score at 70 (because our baseline extraction may be incomplete)
- Continue processing normally

---

## Responsibility Verb Extraction

From the Responsibilities section, extract the main action verbs to understand what the role actually does:

Common patterns:
- "Build and maintain X" → verbs: Build, maintain
- "Collaborate with X to Y" → verbs: collaborate
- "Define and track metrics" → verbs: define, track
- "Present findings to stakeholders" → verbs: present

These verb patterns guide the rewriting in Phase 5: ensure the optimized resume uses verbs that mirror the JD's expected behaviors.

---

## De-noising Rules

Do NOT extract the following as keywords or requirements:

1. **Benefits section phrases:** "competitive salary", "health insurance", "remote work", "unlimited PTO", "stock options"
2. **Culture section phrases:** "fast-paced environment", "collaborative culture", "passionate team", "data-driven culture"
3. **Legal boilerplate:** "equal opportunity employer", "will not discriminate", "reasonable accommodation"
4. **Generic phrases:** "strong communication skills" (unless very specifically repeated and clearly a core requirement), "detail-oriented", "self-starter"

**Exception:** If a generic phrase appears in the Requirements section AND appears ≥ 3 times total in the JD, it may genuinely be important — extract it with LOW weight and flag for user review.

---

## Output to Claude

After parsing the JD, you should have a clear mental model of:
1. What are the top 5 "must have" keywords by frequency
2. What specific verbs describe daily work in this role
3. Any 校招 signals
4. Confidence level of the extraction
5. Which sections were skipped (Benefits/Culture)
