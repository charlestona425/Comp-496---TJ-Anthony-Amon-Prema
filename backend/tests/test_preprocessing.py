import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from compliance_engine.preprocessing import extract_clauses, preprocess_text


class PreprocessingTests(unittest.TestCase):
    def test_normalizes_whitespace_and_typography(self):
        self.assertEqual("We're ready. Second sentence.", preprocess_text("  We’re\n ready.\tSecond sentence.  "))

    def test_extracts_stable_sentence_clauses(self):
        clauses = extract_clauses("First sentence. Second sentence!")
        self.assertEqual(["extracted-1", "extracted-2"], [item["clause_id"] for item in clauses])
        self.assertEqual("Second sentence!", clauses[1]["text"])

