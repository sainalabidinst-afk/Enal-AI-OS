"""
Governance Exceptions Tracker
==============================

Tracks all governance rule exceptions: core changes without ADR,
inter-pack imports, boundary violations, and custom approval records.

Usage:
    python benchmarks/governance_exceptions.py --record \
        --rule "core_change_without_adr" \
        --reason "Urgent security fix" \
        --approver "security-team" \
        --file "backend/app/core/security.py"
    python benchmarks/governance_exceptions.py --list
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

TRACKER_DIR = Path(__file__).resolve().parent.parent / "docs" / "governance"
TRACKER_FILE = TRACKER_DIR / "exceptions.jsonl"

RULE_DEFINITIONS: dict[str, dict[str, Any]] = {
    "core_change_without_adr": {
        "description": "Modification to core directories without ADR reference",
        "severity": "high",
        "governance_section": "Core Change Protection (Section 4, 6)",
    },
    "inter_pack_import": {
        "description": "Capability pack importing from another capability pack",
        "severity": "medium",
        "governance_section": "Capability First Rule (Section 1)",
    },
    "boundary_violation": {
        "description": "Import from forbidden module path (e.g., apps → backend.app.core)",
        "severity": "high",
        "governance_section": "Architecture Boundaries (Section 3)",
    },
    "contract_breaking_change": {
        "description": "Modification to contracts/ that breaks backward compatibility",
        "severity": "high",
        "governance_section": "Contract Stability (Section 8)",
    },
    "runtime_bypass": {
        "description": "Direct import from core bypassing runtime facade",
        "severity": "high",
        "governance_section": "Public Surface (Section 3)",
    },
}


def ensure_tracker() -> None:
    TRACKER_DIR.mkdir(parents=True, exist_ok=True)
    if not TRACKER_FILE.exists():
        TRACKER_FILE.write_text("")


def record_exception(
    rule: str,
    reason: str,
    approver: str,
    file: str | None = None,
    expires: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    ensure_tracker()
    if rule not in RULE_DEFINITIONS:
        raise ValueError(f"Unknown rule: {rule}. Available: {list(RULE_DEFINITIONS)}")
    entry = {
        "id": f"GEX-{datetime.now().strftime('%Y%m%d')}-{len(list(TRACKER_FILE.open())) + 1:03d}",
        "rule": rule,
        "rule_description": RULE_DEFINITIONS[rule]["description"],
        "severity": RULE_DEFINITIONS[rule]["severity"],
        "governance_section": RULE_DEFINITIONS[rule]["governance_section"],
        "reason": reason,
        "approver": approver,
        "file": file,
        "expires": expires,
        "timestamp": datetime.now().isoformat(),
        "metadata": metadata or {},
    }
    with open(TRACKER_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    logger.info("Recorded exception %s for rule %s", entry["id"], rule)
    return entry


def list_exceptions(filter_rule: str | None = None, active_only: bool = True) -> list[dict[str, Any]]:
    if not TRACKER_FILE.exists():
        return []
    entries = []
    for line in TRACKER_FILE.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        entry = json.loads(line)
        if filter_rule and entry["rule"] != filter_rule:
            continue
        if active_only:
            exp = entry.get("expires")
            if exp:
                exp_date = datetime.fromisoformat(exp)
                if datetime.now() > exp_date:
                    continue
        entries.append(entry)
    return entries


def report() -> dict[str, Any]:
    entries = list_exceptions(active_only=False)
    active = list_exceptions(active_only=True)
    by_severity: dict[str, int] = {}
    by_rule: dict[str, int] = {}
    for e in entries:
        by_severity[e["severity"]] = by_severity.get(e["severity"], 0) + 1
        by_rule[e["rule"]] = by_rule.get(e["rule"], 0) + 1
    return {
        "total_exceptions": len(entries),
        "active_exceptions": len(active),
        "by_severity": by_severity,
        "by_rule": by_rule,
        "rules": RULE_DEFINITIONS,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Governance Exceptions Tracker")
    parser.add_argument("--record", action="store_true", help="Record a new exception")
    parser.add_argument("--list", action="store_true", help="List all exceptions")
    parser.add_argument("--report", action="store_true", help="Generate summary report")
    parser.add_argument("--rule", type=str, help="Rule ID for exception")
    parser.add_argument("--reason", type=str, help="Reason for exception")
    parser.add_argument("--approver", type=str, help="Approver name/team")
    parser.add_argument("--file", type=str, help="Affected file path")
    parser.add_argument("--expires", type=str, help="Expiration date (ISO 8601)")
    parser.add_argument("--filter-rule", type=str, help="Filter by rule ID")
    args = parser.parse_args()

    if args.record:
        if not all([args.rule, args.reason, args.approver]):
            print("Error: --rule, --reason, and --approver are required for --record")
            sys.exit(1)
        entry = record_exception(
            rule=args.rule,
            reason=args.reason,
            approver=args.approver,
            file=args.file,
            expires=args.expires,
        )
        print(json.dumps(entry, indent=2))
    elif args.list:
        entries = list_exceptions(filter_rule=args.filter_rule)
        print(json.dumps(entries, indent=2))
    elif args.report:
        rpt = report()
        print(json.dumps(rpt, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
