import pytest

from backend.app.core.benchmark.runner import BenchmarkRunner
from backend.app.core.benchmark.models import BenchmarkCase, ExpectedResult


class FakeCase:
    def __init__(self, case_id, vendor, device_type="router", filename="test.txt"):
        self.case_id = case_id
        self.vendor = vendor
        self.device_type = device_type
        self.filename = filename
        self.expected = None


class TestBenchmarkRunner:
    def test_score_case_all_pass(self):
        runner = BenchmarkRunner()
        case = FakeCase("c1", "cisco")
        expected = ExpectedResult(vendor="cisco", device_type="router", findings_min=1, risk_max=5.0, confidence_min=0.8)
        score = runner._score_case(case, expected, findings=2, risk_score=3.0, confidence=0.9, ast={"vendor": "cisco", "findings": [1], "keywords": ["test"]})
        assert score >= 0.6

    def test_score_case_keyword_match(self):
        runner = BenchmarkRunner()
        case = FakeCase("c1", "cisco")
        expected = ExpectedResult(vendor="cisco", device_type="router", findings_min=1, risk_max=5.0, confidence_min=0.8, expected_keywords=["cisco", "firewall"])
        score = runner._score_case(case, expected, findings=2, risk_score=3.0, confidence=0.9, ast={"vendor": "cisco", "findings": [1]})
        assert score >= 0.6

    def test_score_case_no_keywords(self):
        runner = BenchmarkRunner()
        case = FakeCase("c1", "cisco")
        expected = ExpectedResult(vendor="cisco", device_type="router", findings_min=1, risk_max=5.0, confidence_min=0.8)
        score = runner._score_case(case, expected, findings=0, risk_score=10.0, confidence=0.5)
        assert score < 0.6

    def test_capability_score_all_pass(self):
        runner = BenchmarkRunner()
        case = FakeCase("c1", "cisco")
        expected = ExpectedResult(vendor="cisco", device_type="router", findings_min=1, risk_max=5.0, confidence_min=0.8)
        score = runner._capability_score(case, expected, findings=2, risk_score=3.0, confidence=0.9)
        assert score > 0

    def test_compute_capability_breakdown_empty(self):
        runner = BenchmarkRunner()
        case = FakeCase("c1", "cisco")
        expected = ExpectedResult(vendor="cisco", device_type="router")
        breakdown = runner._compute_capability_breakdown(case, expected)
        assert breakdown.vendor == "cisco"

    def test_score_parser_perfect(self):
        runner = BenchmarkRunner()
        case = FakeCase("c1", "cisco")
        expected = ExpectedResult(vendor="cisco", device_type="router")
        ast = {"vendor": "cisco", "findings": [1], "interfaces": ["eth0"]}
        score = runner._score_parser(case, expected, ast=ast)
        assert score == 100.0

    def test_score_parser_no_ast(self):
        runner = BenchmarkRunner()
        case = FakeCase("c1", "cisco")
        expected = ExpectedResult(vendor="cisco", device_type="router")
        score = runner._score_parser(case, expected, ast=None)
        assert score == 0.0

    def test_score_reasoning_perfect(self):
        runner = BenchmarkRunner()
        case = FakeCase("c1", "cisco")
        expected = ExpectedResult(vendor="cisco", device_type="router")
        findings = [
            {"recommendation": "r1", "confidence": 0.9, "evidence": "e1"},
            {"recommendation": "r2", "confidence": 0.8, "evidence": "e2"},
        ]
        score = runner._score_reasoning(case, expected, ast={}, findings_list=findings)
        assert score == 100.0

    def test_score_reasoning_empty(self):
        runner = BenchmarkRunner()
        case = FakeCase("c1", "cisco")
        expected = ExpectedResult(vendor="cisco", device_type="router")
        score = runner._score_reasoning(case, expected, ast={}, findings_list=[])
        assert score == 0.0

    def test_score_evidence_perfect(self):
        runner = BenchmarkRunner()
        case = FakeCase("c1", "cisco")
        expected = ExpectedResult(vendor="cisco", device_type="router")
        findings = [{"evidence": "e1"}, {"evidence": "e2"}]
        score = runner._score_evidence(findings)
        assert score == 100.0

    def test_score_evidence_empty(self):
        runner = BenchmarkRunner()
        score = runner._score_evidence([])
        assert score == 0.0

    def test_score_compliance_present(self):
        runner = BenchmarkRunner()
        score = runner._score_compliance({"compliance_score": 0.95})
        assert score == 95.0

    def test_score_compliance_missing(self):
        runner = BenchmarkRunner()
        score = runner._score_compliance({})
        assert score == 0.0

    def test_score_executive_report_present(self):
        runner = BenchmarkRunner()
        score = runner._score_executive_report({"summary": "report"})
        assert score == 100.0

    def test_score_executive_report_missing(self):
        runner = BenchmarkRunner()
        score = runner._score_executive_report({})
        assert score == 0.0
