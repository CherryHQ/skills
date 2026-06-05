"""
text_utils.py — Shared text normalization utilities.

Both parse_resume.py and write_resume.py import this module to ensure
that paragraph matching uses identical normalization logic.
"""

import re
import unicodedata


def normalize_text(text: str) -> str:
    """
    Normalize text for consistent matching between parse and write phases.

    Operations applied (in order):
    1. Unicode NFKC normalization (converts full-width chars to half-width, etc.)
    2. Strip leading/trailing whitespace
    3. Collapse internal whitespace sequences to single space
    4. Remove zero-width and invisible Unicode characters
    5. Normalize common punctuation variants (curly quotes → straight quotes, em-dash → --)

    Returns the normalized string. Does NOT lowercase — matching is case-sensitive
    to avoid false positives in resume content.
    """
    if not text:
        return ""

    # NFKC normalization: full-width → half-width, ligatures, etc.
    text = unicodedata.normalize("NFKC", text)

    # Remove zero-width and invisible characters
    text = re.sub(r"[\u200b\u200c\u200d\u200e\u200f\ufeff\u00ad]", "", text)

    # Normalize curly/smart quotes to straight quotes
    text = text.replace("\u2018", "'").replace("\u2019", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')

    # Normalize em-dash and en-dash
    text = text.replace("\u2014", "--").replace("\u2013", "-")

    # Normalize ellipsis
    text = text.replace("\u2026", "...")

    # Collapse whitespace (tabs, multiple spaces, non-breaking spaces)
    text = re.sub(r"[\t\u00a0\u3000]+", " ", text)
    text = re.sub(r" {2,}", " ", text)

    # Strip
    text = text.strip()

    return text


def para_full_text(paragraph) -> str:
    """
    Extract and normalize the full text of a python-docx Paragraph object.
    Joins all runs and applies normalize_text.
    """
    raw = "".join(run.text for run in paragraph.runs)
    return normalize_text(raw)


def para_raw_text(paragraph) -> str:
    """
    Extract the raw (un-normalized) full text of a python-docx Paragraph object.
    """
    return "".join(run.text for run in paragraph.runs)


def fuzzy_match(needle: str, haystack: str) -> bool:
    """
    Fuzzy match: normalize both strings, then check if needle is in haystack.
    Used for match_mode='fuzzy' in write_resume.py.
    """
    return normalize_text(needle) in normalize_text(haystack)


def contains_match(needle: str, haystack: str) -> bool:
    """
    Contains match: check if needle (as-is) appears in haystack (as-is).
    Used for match_mode='contains' (default).
    """
    return needle in haystack


def exact_match(needle: str, haystack: str) -> bool:
    """
    Exact match: needle must equal haystack exactly.
    Used for match_mode='exact'.
    """
    return needle == haystack
