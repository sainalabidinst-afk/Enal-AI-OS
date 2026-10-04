"""
Vendor-specific rule sets for cloud providers and tools.

Provides best practice rules, guardrails, and compliance checks for:
- AWS (Well-Architected Framework)
- Azure (Cloud Adoption Framework)
- GCP (Cloud Architecture Framework)
"""

from __future__ import annotations

from typing import Any

AWS_RULES: dict[str, dict[str, Any]] = {
    "iam": {
        "name": "AWS IAM Best Practices",
        "rules": [
            {
                "id": "aws-iam-001",
                "description": "Use least privilege principle for IAM roles",
                "check": "No wildcard permissions in IAM policies",
                "severity": "high",
                "remediation": "Replace Action/Resource wildcards with specific values",
            },
            {
                "id": "aws-iam-002",
                "description": "Enable MFA for root account",
                "check": "Root account has MFA enabled",
                "severity": "critical",
                "remediation": "Enable virtual MFA device for root account",
            },
            {
                "id": "aws-iam-003",
                "description": "Use IAM roles instead of access keys",
                "check": "EC2 instances use IAM roles, not access keys",
                "severity": "medium",
                "remediation": "Attach IAM roles to EC2 instances",
            },
            {
                "id": "aws-iam-004",
                "description": "Rotate credentials regularly",
                "check": "Access keys are rotated within 90 days",
                "severity": "medium",
                "remediation": "Implement credential rotation policy",
            },
        ],
    },
    "vpc": {
        "name": "AWS VPC Best Practices",
        "rules": [
            {
                "id": "aws-vpc-001",
                "description": "Use private subnets for backend resources",
                "check": "Backend resources in private subnets",
                "severity": "high",
                "remediation": "Move databases and app servers to private subnets",
            },
            {
                "id": "aws-vpc-002",
                "description": "Enable VPC Flow Logs",
                "check": "VPC Flow Logs enabled for all subnets",
                "severity": "medium",
                "remediation": "Enable VPC Flow Logs to CloudWatch",
            },
            {
                "id": "aws-vpc-003",
                "description": "Use Network ACLs as security layers",
                "check": "Network ACLs configured for defense in depth",
                "severity": "medium",
                "remediation": "Add stateless firewall rules at subnet level",
            },
            {
                "id": "aws-vpc-004",
                "description": "Implement least privilege security groups",
                "check": "Security groups restrict traffic to required ports",
                "severity": "high",
                "remediation": "Remove 0.0.0.0/0 access except for HTTP/HTTPS",
            },
        ],
    },
    "compute": {
        "name": "AWS Compute Best Practices",
        "rules": [
            {
                "id": "aws-compute-001",
                "description": "Use Auto Scaling for high availability",
                "check": "Auto Scaling groups configured with min/max/desired",
                "severity": "high",
                "remediation": "Configure Auto Scaling with appropriate thresholds",
            },
            {
                "id": "aws-compute-002",
                "description": "Use appropriate instance types",
                "check": "Instance types match workload requirements",
                "severity": "medium",
                "remediation": "Right-size instances based on utilization metrics",
            },
            {
                "id": "aws-compute-003",
                "description": "Enable detailed monitoring",
                "check": "CloudWatch detailed monitoring enabled",
                "severity": "low",
                "remediation": "Enable 1-minute metrics for critical instances",
            },
        ],
    },
    "monitoring": {
        "name": "AWS CloudWatch Best Practices",
        "rules": [
            {
                "id": "aws-mon-001",
                "description": "Set up CloudWatch alarms for critical metrics",
                "check": "Alarms configured for CPU, memory, disk, network",
                "severity": "high",
                "remediation": "Create CloudWatch alarms with SNS notifications",
            },
            {
                "id": "aws-mon-002",
                "description": "Enable GuardDuty for threat detection",
                "check": "GuardDuty enabled in all regions",
                "severity": "high",
                "remediation": "Enable GuardDuty and configure SNS alerts",
            },
            {
                "id": "aws-mon-003",
                "description": "Centralize logging with CloudWatch Logs",
                "check": "All application logs sent to CloudWatch",
                "severity": "medium",
                "remediation": "Configure CloudWatch Logs agent on all instances",
            },
        ],
    },
}

AZURE_RULES: dict[str, dict[str, Any]] = {
    "identity": {
        "name": "Azure Identity Best Practices",
        "rules": [
            {
                "id": "azure-id-001",
                "description": "Use Azure AD for authentication",
                "check": "No service principal secrets in code",
                "severity": "critical",
                "remediation": "Use managed identities instead of secrets",
            },
            {
                "id": "azure-id-002",
                "description": "Implement least privilege RBAC",
                "check": "No owner roles assigned to non-admin users",
                "severity": "high",
                "remediation": "Assign built-in roles with minimal permissions",
            },
            {
                "id": "azure-id-003",
                "description": "Enable MFA for all users",
                "check": "MFA enforced for all users",
                "severity": "high",
                "remediation": "Enable conditional access with MFA",
            },
        ],
    },
    "network": {
        "name": "Azure Network Best Practices",
        "rules": [
            {
                "id": "azure-net-001",
                "description": "Use NSGs for network segmentation",
                "check": "NSGs applied to all subnets",
                "severity": "high",
                "remediation": "Apply NSGs with least privilege rules",
            },
            {
                "id": "azure-net-002",
                "description": "Enable Azure Firewall",
                "check": "Azure Firewall deployed for egress filtering",
                "severity": "medium",
                "remediation": "Deploy Azure Firewall with forced tunneling",
            },
        ],
    },
}

GCP_RULES: dict[str, dict[str, Any]] = {
    "iam": {
        "name": "GCP IAM Best Practices",
        "rules": [
            {
                "id": "gcp-iam-001",
                "description": "Use service accounts with least privilege",
                "check": "No overly permissive IAM roles",
                "severity": "high",
                "remediation": "Apply principle of least privilege to service accounts",
            },
            {
                "id": "gcp-iam-002",
                "description": "Enable workload identity",
                "check": "GKE workloads use Workload Identity",
                "severity": "medium",
                "remediation": "Migrate from service account keys to Workload Identity",
            },
        ],
    },
    "compute": {
        "name": "GCP Compute Best Practices",
        "rules": [
            {
                "id": "gcp-comp-001",
                "description": "Use committed use discounts",
                "check": "Committed use contracts for steady-state workloads",
                "severity": "low",
                "remediation": "Purchase 1-year or 3-year committed use contracts",
            },
            {
                "id": "gcp-comp-002",
                "description": "Enable autoscaling for GKE",
                "check": "Horizontal pod autoscaling configured",
                "severity": "medium",
                "remediation": "Configure HPA with appropriate metrics and limits",
            },
        ],
    },
}


def get_vendor_rules(vendor: str) -> dict[str, dict[str, Any]]:
    """Get rules for a specific vendor."""
    vendor_lower = vendor.lower()
    if "aws" in vendor_lower:
        return AWS_RULES
    elif "azure" in vendor_lower:
        return AZURE_RULES
    elif "gcp" in vendor_lower or "google" in vendor_lower:
        return GCP_RULES
    return {}


def evaluate_against_vendor_rules(
    config: dict[str, Any] | str,
    vendor: str,
    categories: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Evaluate a configuration against vendor-specific rules.

    ``config`` may be a structured config dict or a raw text blob (for example
    LLM output being checked); every rule probe works off ``str(config)``.
    """
    rules = get_vendor_rules(vendor)
    if not rules:
        return []

    violations = []
    for category, rule_set in rules.items():
        if categories and category not in categories:
            continue
        for rule in rule_set.get("rules", []):
            violation = _check_rule(rule, config)
            if violation:
                violations.append(violation)
    return violations


def _check_rule(rule: dict[str, Any], config: dict[str, Any] | str) -> dict[str, Any] | None:
    """Check a single rule against configuration. Returns violation or None."""
    rule_id = rule.get("id", "")
    check = rule.get("check", "").lower()

    if "wildcard" in check and _has_wildcard(config):
        return {
            "rule_id": rule_id,
            "description": rule.get("description"),
            "severity": rule.get("severity"),
            "remediation": rule.get("remediation"),
            "status": "failed",
        }

    if "mfa" in check and not _has_mfa(config):
        return {
            "rule_id": rule_id,
            "description": rule.get("description"),
            "severity": rule.get("severity"),
            "remediation": rule.get("remediation"),
            "status": "failed",
        }

    if "monitoring" in check and not _has_monitoring(config):
        return {
            "rule_id": rule_id,
            "description": rule.get("description"),
            "severity": rule.get("severity"),
            "remediation": rule.get("remediation"),
            "status": "failed",
        }

    return None


def _has_wildcard(config: dict[str, Any] | str) -> bool:
    """Check if config contains wildcard permissions."""
    config_str = str(config).lower()
    return '"action": "*"' in config_str or '"resource": "*"' in config_str


def _has_mfa(config: dict[str, Any] | str) -> bool:
    """Check if MFA is enabled in config."""
    config_str = str(config).lower()
    return "mfa" in config_str and "enabled" in config_str


def _has_monitoring(config: dict[str, Any] | str) -> bool:
    """Check if monitoring is enabled in config."""
    config_str = str(config).lower()
    return "cloudwatch" in config_str or "monitoring" in config_str
