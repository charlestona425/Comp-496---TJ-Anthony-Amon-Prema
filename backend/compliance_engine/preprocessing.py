"""Text normalization and baseline clause extraction for policy submissions."""

from __future__ import annotations

import re


def preprocess_text(text: str) -> str:
    """Normalize whitespace and common typography without changing meaning."""
    normalized = text.replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    return re.sub(r"\s+", " ", normalized).strip()


def extract_clauses(text: str) -> list[dict[str, object]]:
    """Create stable, sentence-level clauses when NLP segmentation is unavailable."""
    cleaned = preprocess_text(text)
    clauses = []
    cursor = 0
    for index, sentence in enumerate(re.split(r"(?<=[.!?])\s+", cleaned)):
        if not sentence:
            continue
        start = cleaned.find(sentence, cursor)
        end = start + len(sentence)
        cursor = end
        clauses.append({"clause_id": f"extracted-{index + 1}", "text": sentence, "start_offset": start, "end_offset": end})
    return clauses
