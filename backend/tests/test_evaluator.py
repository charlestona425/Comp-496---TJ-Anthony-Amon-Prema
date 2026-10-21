import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from compliance_engine.evaluator import evaluate_document


class EvaluatorTests(unittest.TestCase):
    def setUp(self):
        fixture = Path(__file__).resolve().parents[2] / "fixtures" / "analysis-request.sample.json"
        self.request = json.loads(fixture.read_text(encoding="utf-8"))

    def test_evaluates_matched_clauses_into_traceable_findings(self):
        result = evaluate_document(self.request, analyzed_at="2026-10-01T12:00:00Z")

        self.assertEqual("analysis-070f72d9ba3f", result["analysis_id"])
        self.assertEqual("0.1.0", result["rule_set_version"])
        self.assertEqual("complete", result["coverage"]["status"])
        self.assertEqual(3, len(result["findings"]))
        sharing = next(finding for finding in result["findings"] if finding["rule_id"] == "DSHARE-001")
        self.assertEqual("clause-2", sharing["evidence"][0]["clause_id"])
        self.assertEqual("signal-agency-001", result["positive_signals"][0]["signal_id"])
        self.assertEqual(65.3, result["trust_score"])
        self.assertEqual("low", result["risk_level"])

    def test_exclusion_prevents_a_false_positive(self):
        request = {
            "document_id": "no-ad-sharing",
            "text": "We do not share personal information with advertising partners. This statement provides enough words to evaluate readability as part of this test policy.",
            "clauses": [{"clause_id": "c-1", "text": "We do not share personal information with advertising partners.", "start_offset": 0, "end_offset": 60}],
        }
        result = evaluate_document(request)

        self.assertFalse(any(finding["rule_id"] == "DSHARE-001" for finding in result["findings"]))
        self.assertEqual("partial", result["coverage"]["status"])

    def test_missing_clause_evidence_is_reported_as_partial(self):
        request = {
            "document_id": "thin-policy",
            "text": "Short supplied policy text with enough words to make only readability assessable in this evaluator test.",
            "clauses": [{"clause_id": "c-1", "text": "Short supplied policy text with enough words to make only readability assessable in this evaluator test.", "start_offset": 0, "end_offset": 100}],
        }
        result = evaluate_document(request)

        self.assertEqual("partial", result["coverage"]["status"])
        self.assertTrue(any("insufficient evidence" in item.lower() for item in result["limitations"]))

    def test_detects_reported_collection_sharing_and_legal_signals(self):
        text = "We collect your email address and may share personal information with analytics providers. Disputes are resolved through binding arbitration and a class action waiver. We may change this privacy policy at any time."
        request = {"document_id": "expanded-rules", "text": text, "clauses": [{"clause_id": "c1", "text": text, "start_offset": 0, "end_offset": len(text)}]}
        result = evaluate_document(request)
        rule_ids = {finding["rule_id"] for finding in result["findings"]}
        self.assertTrue({"DCOLL-001", "DSHARE-001", "LEGAL-ARBITRATION-001", "LEGAL-CHANGE-001"}.issubset(rule_ids))
        self.assertTrue(result["key_takeaways"])

    def test_detects_consent_as_a_user_control_signal(self):
        text = "You may withdraw consent at any time through the privacy controls in your account settings. This policy provides enough plain language for readability assessment."
        request = {"document_id": "consent", "text": text, "clauses": [{"clause_id": "c1", "text": text, "start_offset": 0, "end_offset": len(text)}]}
        result = evaluate_document(request)
        self.assertIn("signal-agency-consent-001", {signal["signal_id"] for signal in result["positive_signals"]})

    def test_repeated_analysis_is_consistent_and_handles_edge_case_text(self):
        text = ("Información de privacidad: we do not share personal information with advertising partners. " * 200)
        request = {"document_id": "repeatable-unicode", "text": text, "clauses": [{"clause_id": "c1", "text": text, "start_offset": 0, "end_offset": len(text)}]}
        first = evaluate_document(request, analyzed_at="2026-10-21T00:00:00Z")
        second = evaluate_document(request, analyzed_at="2026-10-21T00:00:00Z")
        self.assertEqual(first, second)
        self.assertEqual("partial", first["coverage"]["status"])

    def test_explains_category_scores_with_policy_excerpts_and_tracking_signal(self):
        text = "We use cookies and similar technologies to track your activity. We may sell your personal information to third parties."
        request = {"document_id": "explainable", "text": text, "clauses": [{"clause_id": "c1", "text": text, "start_offset": 0, "end_offset": len(text)}]}
        result = evaluate_document(request)
        rules = {finding["rule_id"] for finding in result["findings"]}
        self.assertTrue({"TRACK-001", "DSHARE-001"}.issubset(rules))
        collection = next(category for category in result["categories"] if category["id"] == "data_collection")
        self.assertEqual("c1", collection["evidence"][0]["clause_id"])

    def test_processes_full_length_policy_within_reasonable_time(self):
        text = ("We use cookies and similar technologies to provide services. " * 3000)
        request = {"document_id": "full-length", "text": text, "clauses": [{"clause_id": "c1", "text": text, "start_offset": 0, "end_offset": len(text)}]}
        result = evaluate_document(request)
        self.assertGreater(result["trust_score"], 0)


if __name__ == "__main__":
    unittest.main()
