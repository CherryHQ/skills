---
name: template-skill
description: A clear description of what this skill does and when to use it. Include specific trigger phrases like "do X" or "help me with Y". Also include negative triggers — "do NOT use when..." — to prevent false activations.
---

# Skill Name

## Overview

One-paragraph summary of what this skill enables Claude to do.

## When to Use

Specific contexts and user phrases that should trigger this skill:
- User says "phrase 1" or "phrase 2"
- User pastes a file of type X
- User asks for workflow Y

## When NOT to Use

- Do not use for general questions about Z
- Do not use when the user wants to do A (use other-skill instead)

---

## Workflow

### Step 1: Understand Input

What inputs does this skill accept? What format? What are the required vs optional fields?

### Step 2: Process

The core logic. Break into numbered steps if complex.

### Step 3: Deliver Output

What does the output look like? Format, length, structure.

---

## Examples

### Example 1: Basic Usage

**User:** "Do X with this data"

**Claude:** [Shows how the skill processes and responds]

### Example 2: Edge Case

**User:** "Do X but with Y constraint"

**Claude:** [Shows how the skill handles the variation]

---

## Guidelines

- Guideline 1: always do X before Y
- Guideline 2: never assume Z
- Guideline 3: if ambiguous, ask for clarification rather than guessing

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/config.md` | Configuration values, API endpoints, field schemas |
| `references/sop.md` | Detailed standard operating procedure |

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Error X | Usually means Y | Do Z |
