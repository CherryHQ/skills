#!/usr/bin/env python3
"""
validate_input.py — Input validation for cv-expert plugin.

Usage:
  python3 validate_input.py \
    --file "/path/to/resume.docx" \
    --jd-text "Full job description text..." \
    --target-role "Data Analyst Intern" \
    --target-company "Amazon" \
    [--min-jd-chars 80]

Exit codes:
  0 = valid (stdout contains JSON with valid=true)
  1 = invalid (stdout contains JSON with valid=false, errors list non-empty)

Output is always valid JSON to stdout.
"""

import argparse
import json
import os
import sys


def validate(file_path: str, jd_text: str, target_role: str, target_company: str, min_jd_chars: int) -> dict:
    errors = []
    warnings = []
    file_info = None
    jd_info = None
    target_info = None

    # ── Validate resume file ──────────────────────────────────────────────────
    if not file_path:
        errors.append("Resume file path is required.")
    else:
        file_path = file_path.strip()
        if not os.path.exists(file_path):
            errors.append(f"File not found: {file_path}")
        else:
            size_bytes = os.path.getsize(file_path)
            _, ext = os.path.splitext(file_path)
            ext = ext.lower()

            file_info = {
                "path": file_path,
                "size_bytes": size_bytes,
                "exists": True,
                "extension": ext,
            }

            if ext == ".pdf":
                errors.append(
                    "PDF files are not supported in V1. Please save your resume as .docx and try again."
                )
            elif ext == ".doc":
                errors.append(
                    "Legacy .doc format is not supported. Please open the file in Word and save as .docx."
                )
            elif ext != ".docx":
                errors.append(
                    f"Unsupported file extension '{ext}'. Only .docx files are accepted."
                )
            else:
                if size_bytes > 10 * 1024 * 1024:
                    warnings.append(f"File is large ({size_bytes // 1024 // 1024}MB); parsing may take a moment.")

    # ── Validate JD text ──────────────────────────────────────────────────────
    if not jd_text or not jd_text.strip():
        errors.append("JD text is empty. Please paste the full job description.")
        jd_info = {"char_count": 0, "is_empty": True}
    else:
        jd_text_stripped = jd_text.strip()
        char_count = len(jd_text_stripped)
        jd_info = {"char_count": char_count, "is_empty": False}
        if char_count < min_jd_chars:
            errors.append(
                f"JD text is too short ({char_count} chars, minimum {min_jd_chars}). "
                "Please paste the complete job description."
            )

    # ── Validate target role and company ─────────────────────────────────────
    target_role = (target_role or "").strip()
    target_company = (target_company or "").strip()

    if not target_role:
        errors.append("Target role title is required (e.g., 'Data Analyst Intern').")
    if not target_company:
        errors.append("Target company name is required (e.g., 'Amazon').")

    if target_role or target_company:
        target_info = {
            "role": target_role or None,
            "company": target_company or None,
        }

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "file_info": file_info,
        "jd_info": jd_info,
        "target_info": target_info,
    }


def main():
    parser = argparse.ArgumentParser(description="Validate cv-expert inputs.")
    parser.add_argument("--file", required=True, help="Path to resume .docx file")
    parser.add_argument("--jd-text", required=True, help="Full JD text string")
    parser.add_argument("--target-role", default="", help="Target role title")
    parser.add_argument("--target-company", default="", help="Target company name")
    parser.add_argument("--min-jd-chars", type=int, default=80, help="Minimum JD character count")
    args = parser.parse_args()

    result = validate(
        file_path=args.file,
        jd_text=args.jd_text,
        target_role=args.target_role,
        target_company=args.target_company,
        min_jd_chars=args.min_jd_chars,
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
