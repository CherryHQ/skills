# Test Case 3: Error Handling (7 Scenarios)

Run each scenario directly with the Python scripts to verify error handling.

---

## 3a: File not found

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/cv-expert/scripts/validate_input.py \
  --file "/nonexistent/path/resume.docx" \
  --jd-text "$(cat mock_jd_校招.txt)" \
  --target-role "Data Analyst Intern" \
  --target-company "Amazon"
```

**Expected:**
- Exit code: 1
- `valid: false`
- `errors: ["File not found: /nonexistent/path/resume.docx"]`
- Claude behavior: show the error, loop back to Phase 0 Step C, ask for correct path

---

## 3b: JD too short (< 80 chars)

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/cv-expert/scripts/validate_input.py \
  --file "/path/to/valid/resume.docx" \
  --jd-text "Data analyst job" \
  --target-role "Analyst" \
  --target-company "Amazon"
```

**Expected:**
- Exit code: 1
- `valid: false`
- `errors: ["JD text is too short (16 chars, minimum 80)..."]`
- Claude behavior: loop back to Phase 0 Step B, ask user to paste complete JD

---

## 3c: target_company empty

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/cv-expert/scripts/validate_input.py \
  --file "/path/to/valid/resume.docx" \
  --jd-text "$(cat mock_jd_校招.txt)" \
  --target-role "Data Analyst Intern" \
  --target-company ""
```

**Expected:**
- Exit code: 1
- `valid: false`
- `errors: ["Target company name is required (e.g., 'Amazon')."]`
- Claude behavior: loop back to Phase 0 Step A, ask for company name only

---

## 3d: JD URL fetch returns < 300 chars

Simulate by using a URL that returns minimal content.

**Claude behavior (not script-based):**
- WebFetch returns a short response
- Claude detects `len(extracted_text) < 300`
- Tells user: "无法从该URL提取足够的JD内容（提取到 X 字符，需要至少300字符）。请直接粘贴JD文本。"
- Loops back to Phase 0 Step B, asks for paste

---

## 3e: PDF file path provided

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/cv-expert/scripts/validate_input.py \
  --file "/path/to/resume.pdf" \
  --jd-text "$(cat mock_jd_校招.txt)" \
  --target-role "Analyst" \
  --target-company "Amazon"
```

**Expected:**
- Exit code: 1
- `valid: false`
- `errors: ["PDF files are not supported in V1. Please save your resume as .docx and try again."]`
- Claude behavior: explain the limitation, offer to proceed once user provides .docx

---

## 3f: Legacy .doc file provided

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/cv-expert/scripts/validate_input.py \
  --file "/path/to/resume.doc" \
  --jd-text "$(cat mock_jd_校招.txt)" \
  --target-role "Analyst" \
  --target-company "Amazon"
```

**Expected:**
- Exit code: 1
- `valid: false`
- `errors: ["Legacy .doc format is not supported. Please open the file in Word and save as .docx."]`
- Claude behavior: give specific instruction (File → Save As → .docx in Word)

---

## 3g: Patch with non-existent para_id

Create a minimal `bad_patches.json`:
```json
{
  "patch_version": "1.1",
  "patches": [
    {
      "patch_id": "p001",
      "type": "replace_text",
      "target_para_id": "sec_99_p99",
      "original_text": "Does not exist",
      "match_mode": "contains",
      "occurrence_index": 0,
      "replacement_text": "This should fail gracefully",
      "comment": "Test patch",
      "comment_author": "Test",
      "comment_initials": "T",
      "quant_label": null,
      "jd_requirement_ref": "Test",
      "dimension": "keyword"
    },
    {
      "patch_id": "p002",
      "type": "comment_only",
      "target_para_id": "sec_0_p0",
      "comment": "This should succeed even though p001 failed",
      "comment_author": "Test",
      "comment_initials": "T",
      "quant_label": null,
      "jd_requirement_ref": "Test",
      "dimension": "keyword"
    }
  ]
}
```

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/cv-expert/scripts/write_resume.py \
  --input "/path/to/resume.docx" \
  --patches "/tmp/bad_patches.json" \
  --output "/tmp/test_output.docx" \
  --backup "/tmp/test_backup.docx"
```

**Expected:**
- `patches_applied: 1` (p002 succeeds)
- `patches_failed: 1`
- `failed_patch_ids: ["p001"]`
- `success: true` (partial success, not complete failure)
- Claude behavior: report which patches failed and why, output file still generated
