"""Explainable, rule-based privacy-policy assessment components."""

from .scoring import CATEGORY_ORDER, calculate_score
from .evaluator import evaluate_document
from .preprocessing import extract_clauses, preprocess_text

__all__ = ["CATEGORY_ORDER", "calculate_score", "evaluate_document", "extract_clauses", "preprocess_text"]
