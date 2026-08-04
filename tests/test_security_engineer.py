"""
Security Engineer Golden Tests
===============================

Tests for the Security Engineer Capability Pack modules:
OWASP analyzer, secret detector, vulnerability scanner,
threat modeler, hardening reviewer, compliance mapper,
dependency auditor, and the full engine pipeline.
"""
from __future__ import annotations

import json
import pytest

from apps.security_engineer.schemas import (
    AssessmentType,
    Finding,
    SecretFinding,
    SecretType,
    Severity,
    SecurityAssessmentRequest,
    SecurityAssessmentReport,
    SecuritySummary,
    ThreatCategory,
    ThreatModelEntry,
    ThreatModelResult,
    ComplianceReport,
    ComplianceStandard,
)
from apps.security_engineer.engine import SecurityEngineerEngine
from apps.security_engineer.owasp_analyzer import OWASPAnalyzer
from apps.security_engineer.secret_detector import SecretDetector
from apps.security_engineer.vulnerability_scanner import VulnerabilityScanner
from apps.security_engineer.threat_modeler import ThreatModeler
from apps.security_engineer.hardening_reviewer import HardeningReviewer
from apps.security_engineer.compliance_mapper import ComplianceMapper
from apps.security_engineer.dependency_auditor import DependencyAuditor


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def engine():
    return SecurityEngineerEngine()

@pytest.fixture
def owasp():
    return OWASPAnalyzer()

@pytest.fixture
def secret_detector():
    return SecretDetector()

@pytest.fixture
def vuln_scanner():
    return VulnerabilityScanner()

@pytest.fixture
def threat_modeler():
    return ThreatModeler()

@pytest.fixture
def hardening():
    return HardeningReviewer()

@pytest.fixture
def compliance():
    return ComplianceMapper()

@pytest.fixture
def dep_auditor():
    return DependencyAuditor()


# ---------------------------------------------------------------------------
# OWASP Analyzer Tests
# ---------------------------------------------------------------------------

class TestOWASPAnalyzer:
    def test_sql_injection_fstring(self, owasp):
        code = 'query = f"SELECT * FROM users WHERE id = {user_id}"'
        findings = owasp.analyze(code, language="python")
        assert len(findings) >= 1
        categories = [f.category for f in findings]
        assert any("Injection" in c for c in categories)

    def test_command_injection_os_system(self, owasp):
        code = "import os\nos.system(cmd)"
        findings = owasp.analyze(code, language="python")
        assert len(findings) >= 1
        assert any("Injection" in f.category for f in findings)

    def test_xss_innerhtml(self, owasp):
        code = "element.innerHTML = userInput;"
        findings = owasp.analyze(code, language="javascript")
        assert len(findings) >= 1

    def test_ssrf_requests_get(self, owasp):
        code = "import requests\nrequests.get(url)"
        findings = owasp.analyze(code, language="python")
        assert len(findings) >= 1
        assert any("A10:2021" in f.category or "Server-Side Request Forgery" in f.category or "unsanitized URL" in f.title for f in findings)

    def test_weak_crypto_md5(self, owasp):
        code = "import hashlib\nhashlib.md5(data)"
        findings = owasp.analyze(code, language="python")
        assert len(findings) >= 1
        assert any("Cryptographic" in f.category for f in findings)

    def test_insecure_ssl_verify_false(self, owasp):
        code = "requests.get(url, verify=False)"
        findings = owasp.analyze(code, language="python")
        assert len(findings) >= 1

    def test_eval_detection(self, owasp):
        code = "result = eval(user_input)"
        findings = owasp.analyze(code, language="python")
        assert len(findings) >= 1
        assert any("eval" in f.title.lower() for f in findings)

    def test_exec_detection(self, owasp):
        code = "exec(code_string)"
        findings = owasp.analyze(code, language="python")
        assert len(findings) >= 1
        assert any("exec" in f.title.lower() for f in findings)

    def test_clean_code_no_findings(self, owasp):
        code = "def hello(name):\n    return f'Hello, {name}!'"
        findings = owasp.analyze(code, language="python")
        assert len(findings) == 0

    def test_findings_have_required_fields(self, owasp):
        code = 'cursor.execute(f"SELECT * FROM t WHERE id = {user_id}")'
        findings = owasp.analyze(code, language="python")
        assert len(findings) >= 1
        f = findings[0]
        assert f.id
        assert f.category
        assert f.severity in Severity
        assert f.title
        assert f.description
        assert f.remediation
        assert 0.0 <= f.confidence <= 1.0


# ---------------------------------------------------------------------------
# Secret Detector Tests
# ---------------------------------------------------------------------------

class TestSecretDetector:
    def test_api_key_assignment(self, secret_detector):
        code = 'API_KEY = "sk-1234567890abcdef"'
        findings = secret_detector.scan(code)
        assert len(findings) >= 1
        assert any(f.type == SecretType.api_key for f in findings)

    def test_bearer_token(self, secret_detector):
        code = 'Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U'
        findings = secret_detector.scan(code)
        assert len(findings) >= 1
        assert any(f.type == SecretType.token for f in findings)

    def test_password_assignment(self, secret_detector):
        code = 'password = "SuperSecret123!"'
        findings = secret_detector.scan(code)
        assert len(findings) >= 1
        assert any(f.type == SecretType.password for f in findings)

    def test_aws_access_key(self, secret_detector):
        code = 'AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"'
        findings = secret_detector.scan(code)
        assert len(findings) >= 1

    def test_private_key_block(self, secret_detector):
        code = "-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEA...\n-----END RSA PRIVATE KEY-----"
        findings = secret_detector.scan(code)
        assert len(findings) >= 1
        assert any(f.type == SecretType.private_key for f in findings)

    def test_placeholder_filtered(self, secret_detector):
        code = 'password = "changeme"'
        findings = secret_detector.scan(code)
        assert len(findings) == 0

    def test_short_value_filtered(self, secret_detector):
        code = 'token = "abc"'
        findings = secret_detector.scan(code)
        assert len(findings) == 0

    def test_clean_code_no_secrets(self, secret_detector):
        code = "def hello(name):\n    return f'Hello, {name}!'"
        findings = secret_detector.scan(code)
        assert len(findings) == 0

    def test_secret_finding_fields(self, secret_detector):
        code = 'SECRET_KEY = "super_secret_key_12345"'
        findings = secret_detector.scan(code)
        assert len(findings) >= 1
        f = findings[0]
        assert f.id
        assert f.type in SecretType
        assert f.location
        assert f.severity in Severity
        assert f.remediation
        assert 0.0 <= f.confidence <= 1.0


# ---------------------------------------------------------------------------
# Vulnerability Scanner Tests
# ---------------------------------------------------------------------------

class TestVulnerabilityScanner:
    def test_pickle_deserialization(self, vuln_scanner):
        code = "import pickle\ndata = pickle.loads(user_input)"
        findings = vuln_scanner.scan(code, language="python")
        assert len(findings) >= 1
        assert any("deserialization" in f.title.lower() for f in findings)

    def test_hardcoded_credential(self, vuln_scanner):
        code = 'password = "admin123"'
        findings = vuln_scanner.scan(code, language="python")
        assert len(findings) >= 1
        assert any("hardcoded credential" in f.title.lower() for f in findings)

    def test_debug_true(self, vuln_scanner):
        code = "DEBUG = True"
        findings = vuln_scanner.scan(code, language="python")
        assert len(findings) >= 1
        assert any("debug" in f.title.lower() for f in findings)

    def test_ssh_auto_add_policy(self, vuln_scanner):
        code = "ssh.set_missing_host_key_policy(AutoAddPolicy())"
        findings = vuln_scanner.scan(code, language="python")
        assert len(findings) >= 1

    def test_open_redirect(self, vuln_scanner):
        code = "return redirect(request.args.get('next'))"
        findings = vuln_scanner.scan(code, language="python")
        assert len(findings) >= 1

    def test_insecure_random(self, vuln_scanner):
        code = "import random\n token = random.randint(1000, 9999)"
        findings = vuln_scanner.scan(code, language="python")
        assert len(findings) >= 1

    def test_clean_code_no_vulns(self, vuln_scanner):
        code = "def add(a, b):\n    return a + b"
        findings = vuln_scanner.scan(code, language="python")
        assert len(findings) == 0


# ---------------------------------------------------------------------------
# Threat Modeler Tests
# ---------------------------------------------------------------------------

class TestThreatModeler:
    def test_stride_analysis_returns_threats(self, threat_modeler):
        result = threat_modeler.model(
            architecture_description="Web app with user login and database",
            source_code="",
            components=["web", "api", "database"],
            data_flows=["web -> api -> database"],
        )
        assert isinstance(result, ThreatModelResult)
        assert len(result.threats) >= 1

    def test_threat_entries_have_stride_categories(self, threat_modeler):
        result = threat_modeler.model(
            architecture_description="E-commerce platform with payment processing",
            source_code="def delete_user(user_id): db.users.delete(user_id)\ndef process_payment(amount): charge(amount)",
            components=["web", "api", "payment", "database"],
            data_flows=["web -> api -> payment -> database"],
        )
        assert isinstance(result, ThreatModelResult)
        assert len(result.threats) >= 1
        categories = {t.threat_type for t in result.threats}
        assert len(categories) >= 1
        for c in categories:
            assert c in ThreatCategory

    def test_risk_rating_set(self, threat_modeler):
        result = threat_modeler.model(
            architecture_description="Simple static site",
            source_code="",
            components=[],
            data_flows=[],
        )
        assert result.risk_rating in Severity


# ---------------------------------------------------------------------------
# Hardening Reviewer Tests
# ---------------------------------------------------------------------------

class TestHardeningReviewer:
    def test_docker_debug_mode(self, hardening):
        config = "FROM python:3.9\nENV DEBUG=true\nUSER root"
        findings = hardening.review(config, config_type="dockerfile")
        assert len(findings) >= 1

    def test_ssh_root_login(self, hardening):
        config = "ssh_root_login = yes\npassword_authentication = yes"
        findings = hardening.review(config, config_type="ssh")
        assert len(findings) >= 1

    def test_clean_config_no_findings(self, hardening):
        config = "ENV NODE_ENV=production\nPORT=8080"
        findings = hardening.review(config, config_type="docker")
        assert len(findings) == 0


# ---------------------------------------------------------------------------
# Compliance Mapper Tests
# ---------------------------------------------------------------------------

class TestComplianceMapper:
    def test_map_findings_to_standards(self, compliance):
        findings = [
            Finding(
                category="A03:2021-Injection",
                severity=Severity.high,
                title="SQL injection",
                description="SQL injection in query",
                evidence={},
                remediation="Use parameterized queries",
                owasp_mapping="A03:2021-Injection",
            ),
        ]
        report = compliance.map(findings=findings, standards=["pci_dss", "owasp_top10"])
        assert isinstance(report, ComplianceReport)
        assert len(report.standards) >= 1
        assert report.mapped_findings >= 1

    def test_empty_findings(self, compliance):
        report = compliance.map(findings=[], standards=["owasp_top10"])
        assert isinstance(report, ComplianceReport)
        assert report.mapped_findings == 0

    def test_compliance_percentage_populated(self, compliance):
        findings = [
            Finding(
                category="A03:2021-Injection",
                severity=Severity.critical,
                title="SQL injection",
                description="SQL injection",
                evidence={},
                remediation="Fix it",
            ),
        ]
        report = compliance.map(findings=findings, standards=["pci_dss", "hipaa", "iso27001"])
        assert len(report.compliance_percentage) >= 1
        for score in report.compliance_percentage.values():
            assert 0.0 <= score <= 1.0


# ---------------------------------------------------------------------------
# Dependency Auditor Tests
# ---------------------------------------------------------------------------

class TestDependencyAuditor:
    def test_audit_requirements_txt(self, dep_auditor):
        manifest = "django==1.11.0\nrequests==2.6.0"
        findings = dep_auditor.audit(manifest, manifest_type="requirements.txt")
        assert isinstance(findings, list)
        assert len(findings) >= 1

    def test_audit_package_json(self, dep_auditor):
        manifest = '{"dependencies": {"lodash": "4.17.0"}}'
        findings = dep_auditor.audit(manifest, manifest_type="package.json")
        assert isinstance(findings, list)

    def test_clean_manifest(self, dep_auditor):
        manifest = "pytest==8.3.0\npydantic==2.9.0"
        findings = dep_auditor.audit(manifest, manifest_type="requirements.txt")
        assert len(findings) == 0


# ---------------------------------------------------------------------------
# Schemas Tests
# ---------------------------------------------------------------------------

class TestSchemas:
    def test_finding_defaults(self):
        f = Finding(
            category="A03:2021-Injection",
            title="SQL injection",
            description="test",
            evidence={},
        )
        assert f.id
        assert f.severity == Severity.medium
        assert f.confidence == 0.0
        assert f.remediation == ""

    def test_secret_finding_enum(self):
        f = SecretFinding(
            type=SecretType.api_key,
            location="config.py:1",
            evidence={},
        )
        assert f.type == SecretType.api_key
        assert f.severity == SecretFinding.model_fields["severity"].default

    def test_assessment_request_defaults(self):
        req = SecurityAssessmentRequest(
            target_type=AssessmentType.full_review,
            target={"source_code": "print('hello')", "language": "python"},
        )
        assert req.check_secrets is True
        assert req.include_remediation is True
        assert req.standards == ["owasp_top10", "cis"]

    def test_security_summary(self):
        summary = SecuritySummary(
            total_findings=10,
            critical_count=2,
            high_count=3,
            medium_count=4,
            low_count=1,
            overall_risk=Severity.high,
            compliance_score=0.75,
        )
        assert summary.total_findings == 10
        assert summary.overall_risk == Severity.high

    def test_threat_model_entry(self):
        entry = ThreatModelEntry(
            threat_type=ThreatCategory.spoofing,
            component="api",
            description="Spoofing risk",
            likelihood=0.5,
            impact=0.8,
            mitigation="Add authentication",
            confidence=0.9,
        )
        assert entry.threat_type == ThreatCategory.spoofing
        assert entry.likelihood == 0.5


# ---------------------------------------------------------------------------
# Engine Integration Tests
# ---------------------------------------------------------------------------

class TestSecurityEngineerEngine:
    def test_full_review_returns_report(self, engine):
        request = SecurityAssessmentRequest(
            target_type=AssessmentType.full_review,
            target={
                "source_code": 'query = f"SELECT * FROM users WHERE id = {user_id}"',
                "language": "python",
            },
            standards=["owasp_top10", "cis"],
            check_secrets=True,
            check_dependencies=False,
            include_remediation=True,
            include_compliance_mapping=True,
        )
        report = engine.review(request)
        assert isinstance(report, SecurityAssessmentReport)
        assert report.findings is not None
        assert report.secrets is not None
        assert report.summary is not None

    def test_summary_counts_reflect_findings(self, engine):
        request = SecurityAssessmentRequest(
            target_type=AssessmentType.full_review,
            target={
                "source_code": 'import os\nos.system(cmd)\nAPI_KEY = "sk-1234567890"',
                "language": "python",
            },
            standards=["owasp_top10"],
            check_secrets=True,
            check_dependencies=False,
        )
        report = engine.review(request)
        assert report.summary.total_findings == len(report.findings)

    def test_code_review_detects_sql_injection(self, engine):
        request = SecurityAssessmentRequest(
            target_type=AssessmentType.code,
            target={
                "source_code": 'cursor.execute(f"SELECT * FROM t WHERE id = {user_id}")',
                "language": "python",
                "file_path": "app.py",
            },
            standards=["owasp_top10"],
            check_secrets=False,
            check_dependencies=False,
        )
        report = engine.review(request)
        assert len(report.findings) >= 1
        assert any("Injection" in f.category for f in report.findings)

    def test_code_review_detects_secrets(self, engine):
        request = SecurityAssessmentRequest(
            target_type=AssessmentType.code,
            target={
                "source_code": 'SECRET_KEY = "super_secret_key_12345"',
                "language": "python",
                "file_path": "config.py",
            },
            standards=["owasp_top10"],
            check_secrets=True,
            check_dependencies=False,
        )
        report = engine.review(request)
        assert len(report.secrets) >= 1

    def test_clean_code_produces_low_risk(self, engine):
        request = SecurityAssessmentRequest(
            target_type=AssessmentType.code,
            target={
                "source_code": "def add(a, b):\n    return a + b",
                "language": "python",
                "file_path": "utils.py",
            },
            standards=["owasp_top10"],
            check_secrets=True,
            check_dependencies=False,
        )
        report = engine.review(request)
        assert report.summary.overall_risk in (Severity.low, Severity.medium)

    def test_compliance_report_populated(self, engine):
        request = SecurityAssessmentRequest(
            target_type=AssessmentType.full_review,
            target={
                "source_code": 'password = "admin123"',
                "language": "python",
            },
            standards=["pci_dss", "hipaa", "iso27001"],
            check_secrets=True,
            check_dependencies=False,
            include_compliance_mapping=True,
        )
        report = engine.review(request)
        assert len(report.compliance_report.standards) >= 1

    def test_report_to_dict(self, engine):
        request = SecurityAssessmentRequest(
            target_type=AssessmentType.code,
            target={
                "source_code": "print('hello')",
                "language": "python",
            },
            standards=["owasp_top10"],
            check_secrets=False,
            check_dependencies=False,
        )
        report = engine.review(request)
        data = report.to_dict()
        assert isinstance(data, dict)
        assert "findings" in data
        assert "secrets" in data
        assert "summary" in data

    def test_architecture_review_threat_model(self, engine):
        request = SecurityAssessmentRequest(
            target_type=AssessmentType.architecture,
            target={
                "architecture_description": "Web app with payment processing",
                "components": ["web", "api", "payment", "database"],
                "data_flows": ["web -> payment service"],
                "source_code": "def process_payment(amount):\n    charge(amount)\ndef delete_order(order_id):\n    db.orders.delete(order_id)",
            },
            standards=["owasp_top10"],
            check_secrets=False,
            check_dependencies=False,
        )
        report = engine.review(request)
        assert len(report.threat_model.threats) >= 1

    def test_dependency_audit_integration(self, engine):
        request = SecurityAssessmentRequest(
            target_type=AssessmentType.dependency,
            target={
                "manifest_content": "django==1.11.0\nrequests==2.6.0",
                "manifest_type": "re