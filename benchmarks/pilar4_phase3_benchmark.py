"""
Pilar 4 Phase 3 Benchmark
=========================

Benchmarks for Phase 3 Pilar 4 components:
- CapabilityGapDetector
- PackSynthesizer
- AnomalyDetector
- RemediationPlanner
- KnowledgeAbstractor
- FederatedMemorySync

Usage:
    python benchmarks/pilar4_phase3_benchmark.py
"""

from __future__ import annotations

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path

from apps.self_development.anomaly_detector import AnomalyDetector
from apps.self_development.capability_gap_detector import CapabilityGapDetector
from apps.self_development.governance_metrics import governance_metrics
from apps.self_development.knowledge_sync import KnowledgeAbstractor
from apps.self_development.pack_synthesizer import PackSynthesizer
from apps.self_development.remediation_planner import RemediationPlanner
from apps.self_development.schemas import CapabilityProposal


def now_ms() -> float:
    return time.perf_counter() * 1000


async def bench_gap_detector() -> dict:
    detector = CapabilityGapDetector()
    queries = [
        "Jalankan analisis keamanan jaringan",
        "Butuh bantuan menerjemahkan dokumen kontrak",
        "Apa yang bisa kamu lakukan?",
        "Buatkan robot untuk otomatisasi pertanian",
        "Analisis tren inovasi AI",
        "Deploy aplikasi ke Kubernetes",
        "Review kode Python untuk bug",
        "Buatkan dashboard BI untuk penjualan",
    ]
    latencies = []
    results = []
    for q in queries:
        start = now_ms()
        result = detector.detect(q)
        latencies.append(now_ms() - start)
        results.append(
            {
                "query": q,
                "is_gap": result.is_gap,
                "suggested_domain": result.suggested_domain,
                "confidence": result.confidence,
            }
        )
    return {
        "scenarios": len(queries),
        "avg_latency_ms": round(sum(latencies) / len(latencies), 2),
        "max_latency_ms": round(max(latencies), 2),
        "results": results,
    }


async def bench_pack_synthesizer() -> dict:
    synthesizer = PackSynthesizer()
    proposal = CapabilityProposal(
        id="bench-pack",
        name="Benchmark Pack",
        domain="benchmark_pack",
        description="Benchmark capability pack",
        tier="tier_b",
        reuse_potential=0,
        estimated_effort="medium",
        risk="medium",
        confidence=0.8,
        rationale="Benchmark",
        required_packs=[],
        status="draft",
    )
    start = now_ms()
    result = synthesizer.synthesize(proposal)
    latency = now_ms() - start
    return {
        "scenarios": 1,
        "latency_ms": round(latency, 2),
        "schema_created": result.schema_created,
        "engine_created": result.engine_created,
        "worker_created": result.worker_created,
        "tests_scaffolded": result.tests_scaffolded,
        "artifacts": result.artifacts,
    }


async def bench_anomaly_detector() -> dict:
    detector = AnomalyDetector()
    samples = [
        {
            "metric": "cpu_usage",
            "current_value": 95.0,
            "baseline": 50.0,
            "threshold_pct": 20.0,
            "category": "performance",
        },
        {
            "metric": "memory_usage",
            "current_value": 55.0,
            "baseline": 50.0,
            "threshold_pct": 20.0,
            "category": "performance",
        },
        {
            "metric": "error_rate",
            "current_value": 0.15,
            "baseline": 0.01,
            "threshold_pct": 50.0,
            "category": "security",
        },
        {
            "metric": "latency_p95",
            "current_value": 500.0,
            "baseline": 100.0,
            "threshold_pct": 30.0,
            "category": "performance",
        },
        {
            "metric": "disk_usage",
            "current_value": 92.0,
            "baseline": 80.0,
            "threshold_pct": 15.0,
            "category": "infrastructure",
        },
    ]
    latencies = []
    all_anomalies = []
    for s in samples:
        start = now_ms()
        anomaly = detector.detect(**s)
        latencies.append(now_ms() - start)
        if anomaly is not None:
            all_anomalies.append(
                {
                    "metric": anomaly.metric,
                    "severity": anomaly.severity,
                    "deviation_pct": anomaly.deviation_pct,
                }
            )
    batch_start = now_ms()
    detector.detect_batch(samples)
    batch_latency = now_ms() - batch_start
    return {
        "scenarios": len(samples),
        "individual_avg_latency_ms": round(sum(latencies) / len(latencies), 2),
        "batch_latency_ms": round(batch_latency, 2),
        "anomalies_detected": len(all_anomalies),
        "anomalies": all_anomalies,
    }


async def bench_remediation_planner() -> dict:
    from apps.self_development.anomaly_detector import Anomaly

    planner = RemediationPlanner()
    anomalies = [
        Anomaly(
            anomaly_id="bench-anomaly-1",
            category="performance",
            severity="low",
            metric="cpu_usage",
            current_value=95.0,
            baseline=50.0,
            deviation_pct=90.0,
            description="CPU spike",
        ),
        Anomaly(
            anomaly_id="bench-anomaly-2",
            category="security",
            severity="critical",
            metric="error_rate",
            current_value=0.15,
            baseline=0.01,
            deviation_pct=1400.0,
            description="Error rate spike",
        ),
    ]
    latencies = []
    results = []
    for a in anomalies:
        start = now_ms()
        playbook = planner.plan(a)
        latencies.append(now_ms() - start)
        results.append(
            {
                "anomaly_id": a.anomaly_id,
                "severity": a.severity,
                "requires_consent": playbook.requires_consent,
                "steps_count": len(playbook.steps),
            }
        )
    return {
        "scenarios": len(anomalies),
        "avg_latency_ms": round(sum(latencies) / len(latencies), 2),
        "results": results,
    }


async def bench_knowledge_sync() -> dict:
    abstractor = KnowledgeAbstractor()
    payloads = [
        {"text": "Contact admin@example.com for support", "email": "admin@example.com"},
        {"text": "Server IP is 192.168.1.1", "ip": "192.168.1.1"},
        {"text": "Use password=secret123 for login", "password": "secret123"},
        {"text": "Card number 4111-1111-1111-1111", "card": "4111-1111-1111-1111"},
    ]
    latencies = []
    pii_removed_count = 0
    for p in payloads:
        start = now_ms()
        abstracted, removed = abstractor.abstract(p)
        latencies.append(now_ms() - start)
        if removed:
            pii_removed_count += 1
    return {
        "scenarios": len(payloads),
        "avg_latency_ms": round(sum(latencies) / len(latencies), 2),
        "pii_removed_count": pii_removed_count,
        "privacy_violation_rate": round((len(payloads) - pii_removed_count) / len(payloads), 4),
    }


async def bench_governance_metrics() -> dict:
    for _ in range(10):
        governance_metrics.record_pack_synthesis(accepted=True)
    for _ in range(2):
        governance_metrics.record_pack_synthesis(accepted=False)
    for _ in range(8):
        governance_metrics.record_remediation(success=True)
    for _ in range(2):
        governance_metrics.record_remediation(success=False)
    for _ in range(5):
        governance_metrics.record_federated_sync(pii_removed=True)
    for _ in range(3):
        governance_metrics.record_federated_sync(pii_removed=False)
    for _ in range(20):
        governance_metrics.record_gate_latency(150.0 + (_ % 5) * 20)
    snapshot = governance_metrics.snapshot()
    return snapshot


async def main() -> None:
    print("=" * 60)
    print("Pilar 4 Phase 3 Benchmark")
    print("=" * 60)
    print()

    results = {
        "generated_at": datetime.utcnow().isoformat(),
        "benchmarks": {},
    }

    print("[1/6] CapabilityGapDetector...")
    results["benchmarks"]["gap_detector"] = await bench_gap_detector()
    print(f"  Scenarios: {results['benchmarks']['gap_detector']['scenarios']}")
    print(f"  Avg latency: {results['benchmarks']['gap_detector']['avg_latency_ms']}ms")
    print()

    print("[2/6] PackSynthesizer...")
    results["benchmarks"]["pack_synthesizer"] = await bench_pack_synthesizer()
    print(f"  Latency: {results['benchmarks']['pack_synthesizer']['latency_ms']}ms")
    print(f"  Artifacts: {list(results['benchmarks']['pack_synthesizer']['artifacts'].keys())}")
    print()

    print("[3/6] AnomalyDetector...")
    results["benchmarks"]["anomaly_detector"] = await bench_anomaly_detector()
    print(f"  Scenarios: {results['benchmarks']['anomaly_detector']['scenarios']}")
    print(
        f"  Anomalies detected: {results['benchmarks']['anomaly_detector']['anomalies_detected']}"
    )
    print()

    print("[4/6] RemediationPlanner...")
    results["benchmarks"]["remediation_planner"] = await bench_remediation_planner()
    print(f"  Scenarios: {results['benchmarks']['remediation_planner']['scenarios']}")
    print(f"  Avg latency: {results['benchmarks']['remediation_planner']['avg_latency_ms']}ms")
    print()

    print("[5/6] KnowledgeAbstractor...")
    results["benchmarks"]["knowledge_abstractor"] = await bench_knowledge_sync()
    print(f"  Scenarios: {results['benchmarks']['knowledge_abstractor']['scenarios']}")
    print(f"  PII removed: {results['benchmarks']['knowledge_abstractor']['pii_removed_count']}")
    print()

    print("[6/6] GovernanceMetrics...")
    results["benchmarks"]["governance_metrics"] = await bench_governance_metrics()
    snap = results["benchmarks"]["governance_metrics"]
    print(f"  Pack synthesis acceptance rate: {snap['pack_synthesis_acceptance_rate']:.2%}")
    print(f"  Remediation success rate: {snap['remediation_success_rate']:.2%}")
    print(f"  Federated privacy violation rate: {snap['federated_privacy_violation_rate']:.2%}")
    print(f"  Avg gate latency: {snap['avg_gate_latency_ms']:.2f}ms")
    print()

    report_path = Path("benchmarks/reports/pilar4_phase3_benchmark.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Report written: {report_path}")


if __name__ == "__main__":
    asyncio.run(main())
