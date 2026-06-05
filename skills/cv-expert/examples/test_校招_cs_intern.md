# Test Case 1: 校招完整流程（CS 实习生，无 KPI）

## Setup

**JD:** `mock_jd_校招.txt` (Amazon Data Analyst Intern)
**Resume:** Use a mock .docx with the following structure (or your real resume)

### Mock Resume Structure (for testing without a real .docx)

To test with a synthetic docx, create `test_resume_校招.docx` with:

```
马小明
Email: xiaoming@example.com | Phone: 138-0000-0000

EDUCATION
Johns Hopkins University — M.S. Business Analytics | GPA: 3.8 | Aug 2024 – May 2026
Relevant coursework: Machine Learning, Data Mining, Database Systems, Statistics

INTERNSHIP EXPERIENCE
Data Analytics Intern | PricewaterhouseCoopers | Jun 2024 – Aug 2024
• Analyzed financial data for client risk assessment
• Used Excel and PowerPoint to prepare reports for senior management
• Helped team with data collection and cleaning

PROJECTS
Customer Churn Prediction | Machine Learning Course Project
• Built a logistic regression model to predict customer churn
• Preprocessed dataset and trained model using Python

SKILLS
Programming: Python, R, SQL
Visualization: Excel, PowerPoint
Languages: Mandarin (native), English (fluent)
[Note: Skills section is in a table — expected to trigger ATS warning]
```

## Expected Behavior

### Phase 0: Intake
- target_role_title: "Data Analyst Intern"
- target_company: "Amazon"
- target_track: "DA"
- mode: "校招"
- JD: paste mock_jd_校招.txt content
- output_strategy: SAFE (default) or BOOSTED

### Phase 1: Validate
- Should pass with `valid: true`
- No errors

### Phase 2: Parse
- Should detect sections: EDUCATION, INTERNSHIP EXPERIENCE, PROJECTS, SKILLS
- `ats_flags.has_tables: true` (Skills in table)
- `flat_bullets` should contain ~4 bullets

### Phase 3: Diagnose (Expected Scores ~校招 weights)
- Dimension 1 (Eligibility): ~80 — M.S. program matches, no major violations
- Dimension 2 (Keyword): ~50-60 — Python ✅, SQL ✅, Tableau ❌, A/B testing ❌
- Dimension 3 (Impact): ~25 — all bullets activity-based, zero numbers
- Dimension 4 (Competency): ~55 — data analysis ⚠️, visualization ❌, A/B ❌
- Dimension 5 (Story): ~75 — reasonable timeline
- Dimension 6 (Language): ~55 — "helped", "used" are weak verbs
- Dimension 7 (ATS): ~60 — table in skills, no date format issues expected

### Phase 4: Gap Q&A (Expected Questions)
1. Data scale for the PwC internship (records, clients, size?)
2. Any A/B testing in coursework or projects? (maps to high-priority JD keyword)
3. Churn model: accuracy/F1 score? Dataset size?
4. Tableau experience? (JD mentions it specifically)
5. SQL usage: any complex queries? (JD requires SQL with joins/window functions)

### Expected Patches
- 3-5 `replace_text` patches (verb improvements + keyword additions from Q&A answers)
- 2-3 `comment_only` patches (NEED_CONFIRM items, ATS table warning)
- Evidence Mining: PwC bullet "Analyzed financial data" → reframe to include scale/tool/result
- 校招 templates should be offered for data scale and time estimation

### Pass Criteria
✅ No invented company names or project titles
✅ Eligibility Dimension does NOT block the workflow
✅ ATS table warning appears in Dimension 7
✅ 校招 quantification templates offered during Q&A
✅ All Estimate items in SAFE mode go to comment_only
✅ JD-to-Evidence mapping table present in output
✅ 6+ interview follow-up questions grouped by Evidence/Impact/Tradeoff

## How to Run with a Real .docx

Replace the mock structure with your actual .docx path:
```bash
# Step 1: Install dependencies
bash ${CLAUDE_PLUGIN_ROOT}/skills/cv-expert/scripts/setup.sh

# Step 2: Test the validator
python3 ${CLAUDE_PLUGIN_ROOT}/skills/cv-expert/scripts/validate_input.py \
  --file "/path/to/your/resume.docx" \
  --jd-text "$(cat ${CLAUDE_PLUGIN_ROOT}/skills/cv-expert/examples/mock_jd_校招.txt)" \
  --target-role "Data Analyst Intern" \
  --target-company "Amazon"

# Step 3: Test the parser
python3 ${CLAUDE_PLUGIN_ROOT}/skills/cv-expert/scripts/parse_resume.py \
  --input "/path/to/your/resume.docx" \
  --output "/tmp/test_parsed.json"
cat /tmp/test_parsed.json

# Step 4: Full end-to-end via Claude Code
/cv-expert /path/to/your/resume.docx --mode 校招
```
