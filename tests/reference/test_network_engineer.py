import asyncio
import json
from pathlib import Path
from typing import Any
import re

from apps.network_engineer import get_app


GOLDEN_DIR = Path(__file__).resolve().parents[2] / "golden" / "mikrotik"


def load_config(scenario: str) -> str:
    path = GOLDEN_DIR / scenario / "config.rsc"
    if not path.exists():
        raise FileNotFoundError(f"Missing golden config: {path}")
    return path.read_text(encoding="utf-8")


def load_expected(scenario: str, name: str) -> Any:
    path = GOLDEN_DIR / scenario / name
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    if name.endswith(".json"):
        return json.loads(text)
    return text


def extract_keywords(text: str) -> list[str]:
    text = text.lower()
    stop_words = {"the", "is", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "from", "as", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did", "will", "would", "could", "should", "may", "might", "must", "can", "shall", "not", "no", "nor", "so", "very", "just", "because", "but", "and", "or", "yet", "if", "then", "than", "too", "very", "s", "t", "don", "now"}
    words = re.findall(r"[a-z0-9\-]+", text)
    return [w for w in words if len(w) > 3 and w not in stop_words]


SCENARIOS = [
    "home", "office", "hotel", "rt-rw-net", "campus", "isp-small", "isp-medium",
    "isp-large", "mpls", "ospf", "bgp", "capsman", "vlan", "wireguard",
    "hotspot-voucher", "pppoe", "eoip", "vrrp", "dual-wan", "load-balance-pcc",
    "failover", "queue-tree", "simple-queue", "ipv6", "dns-cache",
    "firewall-enterprise", "broken-config", "invalid-syntax", "partial-config",
    "old-v6", "new-v7"
]


async def run_scenario(scenario: str) -> dict[str, Any]:
    app = get_app()
    config_content = load_config(scenario)

    analysis = await app.analyze_config(config_content)
    findings = analysis.get("issues", [])
    summary = analysis.get("summary", {})

    documentation = await app.generate_documentation(config_content)

    return {
        "scenario": scenario,
        "findings_count": len(findings),
        "summary": summary,
        "documentation_generated": bool(documentation.strip()),
        "findings": findings,
    }


async def main() -> int:
    print("Running Network Engineer Golden Tests")
    print("=" * 80)

    results = []
    for scenario in SCENARIOS:
        try:
            result = await run_scenario(scenario)
            results.append(result)
            status = "PASS" if result["findings_count"] > 0 and result["documentation_generated"] else "FAIL"
            print(f"[{status}] {scenario}: findings={result['findings_count']}, docs={'yes' if result['documentation_generated'] else 'no'}")
        except Exception as e:
            print(f"[FAIL] {scenario}: {e}")
            results.append({"scenario": scenario, "error": str(e)})

    print("=" * 80)

    errored = [r for r in results if "error" in r]
    successful = [r for r in results if "error" not in r]
    if not successful:
        print("FAILED: No scenarios completed successfully")
        return 1

    docs_generated = sum(1 for r in successful if r.get("documentation_generated"))
    findings_generated = sum(1 for r in successful if r.get("findings_count", 0) > 0)
    pass_count = sum(
        1
        for r in successful
        if r.get("findings_count", 0) > 0 and r.get("documentation_generated")
    )

    print(f"Scenarios with findings: {findings_generated}/{len(SCENARIOS)}")
    print(f"Documentation generated: {docs_generated}/{len(successful)}")
    print(f"Scenarios passed: {pass_count}/{len(SCENARIOS)}")

    if pass_count == len(SCENARIOS):
        print("SUCCESS: All scenarios produced findings and documentation")
        return 0

    print("FAILED: Some scenarios did not complete successfully")
    return 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
