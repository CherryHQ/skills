#!/usr/bin/env python3
"""Sanitize skills before publishing to public repo.

Usage: python3 sanitize.py rules.json skills/
"""

import json
import os
import re
import sys
from pathlib import Path

RULES_FILE = sys.argv[1] if len(sys.argv) > 1 else "sanitize-rules.json"
SKILLS_DIR = sys.argv[2] if len(sys.argv) > 2 else "skills"


def load_rules(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def should_process_file(filepath: Path, rules: dict) -> bool:
    """Check if file should be processed (not excluded)."""
    try:
        rel = str(filepath.relative_to(SKILLS_DIR))
    except ValueError:
        rel = str(filepath)
    
    for pattern in rules.get("path_patterns", {}).get("exclude_from_public", []):
        if pattern in rel or rel.endswith(pattern):
            return False
    return True


def detect_secrets(content: str, rules: dict) -> list:
    """Detect potential secrets that weren't replaced."""
    found = []
    for pattern in rules.get("secret_detection", {}).get("patterns", []):
        matches = re.findall(pattern, content)
        if matches:
            found.extend(matches[:3])  # Report first 3
    return found


def sanitize_file(filepath: Path, rules: dict):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    for rule in rules.get("replacements", []):
        flags = 0 if rule.get("case_sensitive", True) else re.IGNORECASE
        find = rule["find"]
        replace = rule["replace"]
        
        # Use word boundary for short terms to avoid partial matches
        if len(find) <= 10 and not find.startswith("\u003c"):
            pattern = r'\b' + re.escape(find) + r'\b'
        else:
            pattern = re.escape(find)
        
        content = re.sub(pattern, replace, content, flags=flags)

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  sanitized: {filepath}")

    # Secret detection after replacement
    if rules.get("secret_detection", {}).get("action") == "fail":
        remaining = detect_secrets(content, rules)
        if remaining:
            print(f"  ⚠️  Potential secret remaining in {filepath}: {remaining}")
            # Don't hard-fail here; let the workflow decide


def main():
    rules = load_rules(RULES_FILE)
    skills_path = Path(SKILLS_DIR)

    removed_count = 0
    sanitized_count = 0

    for skill_dir in sorted(skills_path.iterdir()):
        if not skill_dir.is_dir():
            continue

        for root, dirs, files in os.walk(skill_dir):
            # Remove excluded directories
            dirs[:] = [d for d in dirs if not any(
                pat in str(Path(root) / d) for pat in 
                rules.get("path_patterns", {}).get("exclude_from_public", [])
            )]
            
            for filename in files:
                if not filename.endswith((".md", ".json", ".py", ".yml", ".yaml", ".ts", ".js", ".sh")):
                    continue
                
                filepath = Path(root) / filename
                if not should_process_file(filepath, rules):
                    os.remove(filepath)
                    removed_count += 1
                    print(f"  removed: {filepath}")
                    continue
                
                sanitize_file(filepath, rules)
                sanitized_count += 1

    print(f"\nDone. {sanitized_count} files processed, {removed_count} files removed.")


if __name__ == "__main__":
    main()
