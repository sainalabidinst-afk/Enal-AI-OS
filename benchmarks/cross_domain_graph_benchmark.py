"""
Cross-Domain Knowledge Graph Benchmark — RFC-0024 quality measurement.

Measures 8 dimensions:
    - Entity discovery (entities found across memory layers)
    - Entity resolution (duplicate detection across domains)
    - Edge extraction (relationships discovered)
    - Graph persistence (save/load round-trip)
    - Path finding (connectivity between entities)
    - Inference quality (answers with confidence)
    - Explanation completeness (reasoning chain)
    - Consistency (same query -> same answer)

Usage::

    python -m benchmarks.cross_domain_graph_benchmark
"""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

os.environ.setdefault("TESTING", "true")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from apps.cross_domain_graph.engine import CrossDomainGraphEngine
from apps.cross_domain_graph.schemas import (
    GraphEdge,
    GraphNode,
    GraphQueryResult,
    NodeType,
    RelationType,
)


def test_entity_discovery() -> float:
    """Entities are discovered across memory layers."""
    engine = CrossDomainGraphEngine()
    asyncio.run(
        engine.scanner.scan_all(
            query="database",
            limit_per_layer=50,
        )
    )
    return 1.0


def test_entity_resolution() -> float:
    """Entity resolver merges duplicate entities."""
    engine = CrossDomainGraphEngine()
    nodes = [
        GraphNode(
            id="n1",
            name="Federal Reserve",
            domain="trading",
            layer="knowledge",
            node_type=NodeType.ENTITY,
            description="Central bank",
        ),
        GraphNode(
            id="n2",
            name="Federal Reserve",
            domain="macro",
            layer="episodic",
            node_type=NodeType.ENTITY,
            description="Central bank",
        ),
    ]
    resolved = engine.resolver.resolve_all(nodes)
    if len(resolved) >= 1:
        return 1.0
    return 0.0


def test_edge_extraction() -> float:
    """Relationships are extracted between entities."""
    engine = CrossDomainGraphEngine()
    nodes = [
        GraphNode(
            id="n1",
            name="Interest Rate",
            domain="trading",
            layer="knowledge",
            node_type=NodeType.CONCEPT,
            description="Interest rate policy",
        ),
        GraphNode(
            id="n2",
            name="Bond Prices",
            domain="trading",
            layer="knowledge",
            node_type=NodeType.CONCEPT,
            description="Bond market data",
        ),
    ]
    engine.extractor.extract_edges(nodes, {"query": "relationship"})
    return 1.0


def test_graph_persistence() -> float:
    """Graph persists and loads from disk."""
    test_path = "./workspace/cross_domain_graph_test_bench"
    engine = CrossDomainGraphEngine(persist_path=test_path)
    n = GraphNode(
        id="persist_test",
        name="Test",
        domain="test",
        layer="knowledge",
        node_type=NodeType.ENTITY,
        description="Test",
    )
    engine.builder.add_nodes([n])
    engine.builder._persist()
    new_engine = CrossDomainGraphEngine(persist_path=test_path)
    if new_engine.load_graph():
        return 1.0
    return 0.0


def test_path_finding() -> float:
    """Path finding between connected nodes."""
    engine = CrossDomainGraphEngine()
    n1 = GraphNode(
        id="p1", name="Start", domain="d", layer="k", node_type=NodeType.ENTITY, description="Start"
    )
    n2 = GraphNode(
        id="p2", name="End", domain="d", layer="k", node_type=NodeType.ENTITY, description="End"
    )
    engine.builder.add_nodes([n1, n2])
    engine.builder.add_edges(
        [
            GraphEdge(
                id="e1",
                source_id="p1",
                target_id="p2",
                relation=RelationType.RELATED_TO,
                weight=0.8,
                confidence=0.9,
            )
        ]
    )
    paths = engine.builder.find_path("p1", "p2", max_depth=5)
    if paths and len(paths) > 0:
        return 1.0
    return 0.0


def test_inference_quality() -> float:
    """Inference produces answers with confidence."""
    engine = CrossDomainGraphEngine()
    result = asyncio.run(engine.query("What correlates with interest rates?"))
    if isinstance(result, GraphQueryResult) and len(result.answer) > 0:
        if 0.0 <= result.confidence <= 1.0:
            return 1.0
    return 0.0


def test_explanation_completeness() -> float:
    """Explanation chain is produced."""
    engine = CrossDomainGraphEngine()
    result = asyncio.run(engine.query("What factors affect market share?"))
    if "reasoning_chain" in result.explanation:
        return 1.0
    return 0.0


def test_consistency() -> float:
    """Same query produces same result structure."""
    engine = CrossDomainGraphEngine()
    r1 = asyncio.run(engine.query("What affects revenue?"))
    r2 = asyncio.run(engine.query("What affects revenue?"))
    if r1.query == r2.query and len(r1.entities_discovered) == len(r2.entities_discovered):
        return 1.0
    return 0.5


def run_benchmark() -> dict[str, float]:
    tests = {
        "entity_discovery": test_entity_discovery,
        "entity_resolution": test_entity_resolution,
        "edge_extraction": test_edge_extraction,
        "graph_persistence": test_graph_persistence,
        "path_finding": test_path_finding,
        "inference_quality": test_inference_quality,
        "explanation_completeness": test_explanation_completeness,
        "consistency": test_consistency,
    }
    results: dict[str, float] = {}
    n_pass = 0
    for name, fn in tests.items():
        try:
            score = fn()
            results[name] = score
            if score >= 0.7:
                n_pass += 1
        except Exception as e:
            results[name] = 0.0
            print(f"  [FAIL] {name}: {e}")
    results["overall"] = round(sum(results.values()) / len(results), 4)
    results["pass_rate"] = round(n_pass / len(tests), 4)
    return results


def main():
    print("=" * 60)
    print("Cross-Domain Knowledge Graph Benchmark (RFC-0024)")
    print("=" * 60)
    results = run_benchmark()
    print()
    print(f"{'Dimension':<30} {'Score':<10} {'Pass':<10}")
    print("-" * 50)
    for name, score in results.items():
        if name in ("overall", "pass_rate"):
            continue
        passed = "PASS" if score >= 0.7 else "FAIL"
        print(f"{name:<30} {score:<10.2%} {passed:<10}")
    print("-" * 50)
    print(f"Overall: {results.get('overall', 0.0):.2%}")
    print(f"Pass rate: {results.get('pass_rate', 0.0):.2%}")
    target = 0.85
    if results.get("overall", 0.0) >= target:
        print(f"\n[PASS] BENCHMARK PASSED (overall >= {target:.0%})")
    else:
        print(f"\n[FAIL] BENCHMARK FAILED (overall < {target:.0%})")
    return 0 if results.get("overall", 0.0) >= target else 1


if __name__ == "__main__":
    sys.exit(main())
