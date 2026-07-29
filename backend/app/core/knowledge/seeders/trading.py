from __future__ import annotations

from backend.app.core.knowledge.edge import KnowledgeEdge
from backend.app.core.knowledge.graph import KnowledgeGraph
from backend.app.core.knowledge.node import KnowledgeNode
from backend.app.core.knowledge.registry import KnowledgeRegistry
from backend.app.core.knowledge.schema import (
    KnowledgeCategory,
    KnowledgeDomain,
    KnowledgeEntity,
    KnowledgeStatus,
    KnowledgeType,
)


def seed_trading_knowledge(registry: KnowledgeRegistry, graph: KnowledgeGraph) -> None:
    concepts = [
        ("trend", "Trend", "Directional movement of price over time"),
        ("market_structure", "Market Structure", "Higher highs, lower lows, range, breakout"),
        ("liquidity", "Liquidity", "Ability to enter/exit positions without slippage"),
        ("volume", "Volume", "Quantity of traded asset in a period"),
        ("volatility", "Volatility", "Statistical dispersion of returns"),
        ("order_flow", "Order Flow", "Buy/sell pressure and execution flow"),
        ("risk", "Risk", "Exposure to adverse price movement"),
        ("portfolio", "Portfolio", "Collection of positions and capital allocation"),
        ("macro_economy", "Macro Economy", "Interest rates, inflation, GDP, employment"),
        ("correlation", "Correlation", "Statistical relationship between assets"),
        ("economic_calendar", "Economic Calendar", "Scheduled macro events and releases"),
        ("candlestick_pattern", "Candlestick Pattern", "Visual price pattern in OHLC"),
        ("price_action", "Price Action", "Raw price movement without indicators"),
        ("probability", "Probability", "Likelihood of an outcome"),
        ("scenario", "Scenario", "Hypothetical market state or event"),
    ]

    entities: dict[str, KnowledgeEntity] = {}
    for cid, name, description in concepts:
        entity = KnowledgeEntity(
            id=cid,
            domain=KnowledgeDomain.TRADING,
            category=KnowledgeCategory.DOMAIN,
            type=KnowledgeType.CONCEPT,
            name=name,
            description=description,
            status=KnowledgeStatus.VALIDATED,
            confidence=0.9,
            tags=["trading", "domain"],
            source="trading-domain-seed",
            owner="platform",
        )
        registry.register(entity)
        node = KnowledgeNode(
            id=entity.id,
            domain=entity.domain.value,
            category=entity.category.value,
            type=entity.type.value,
            name=entity.name,
            description=entity.description,
            status=entity.status.value,
            confidence=entity.confidence,
            schema_version=entity.schema_version,
            knowledge_version=entity.knowledge_version,
            created_at=entity.created_at.isoformat(),
            updated_at=entity.updated_at.isoformat(),
            tags=list(entity.tags),
            metadata=dict(entity.metadata),
            evidence=list(entity.evidence),
            related_ids=list(entity.related_ids),
            source=entity.source,
            owner=entity.owner,
        )
        graph.add_node(node)
        entities[cid] = entity

    relations = [
        ("trend", "market_structure", "relates_to"),
        ("trend", "momentum", "relates_to"),
        ("trend", "breakout", "relates_to"),
        ("trend", "risk", "relates_to"),
        ("trend", "strategy", "relates_to"),
        ("market_structure", "trend", "contains"),
        ("market_structure", "liquidity", "relates_to"),
        ("market_structure", "risk", "relates_to"),
        ("liquidity", "order_flow", "relates_to"),
        ("liquidity", "portfolio", "relates_to"),
        ("volume", "liquidity", "relates_to"),
        ("volume", "order_flow", "relates_to"),
        ("volume", "candlestick_pattern", "relates_to"),
        ("volatility", "risk", "relates_to"),
        ("volatility", "probability", "relates_to"),
        ("volatility", "scenario", "relates_to"),
        ("order_flow", "liquidity", "relates_to"),
        ("order_flow", "price_action", "relates_to"),
        ("risk", "portfolio", "relates_to"),
        ("risk", "probability", "relates_to"),
        ("portfolio", "correlation", "relates_to"),
        ("portfolio", "macro_economy", "relates_to"),
        ("macro_economy", "economic_calendar", "relates_to"),
        ("macro_economy", "correlation", "relates_to"),
        ("correlation", "portfolio", "relates_to"),
        ("correlation", "probability", "relates_to"),
        ("economic_calendar", "macro_economy", "relates_to"),
        ("economic_calendar", "volatility", "relates_to"),
        ("candlestick_pattern", "price_action", "relates_to"),
        ("candlestick_pattern", "trend", "relates_to"),
        ("price_action", "trend", "relates_to"),
        ("price_action", "market_structure", "relates_to"),
        ("price_action", "order_flow", "relates_to"),
        ("probability", "scenario", "relates_to"),
        ("probability", "risk", "relates_to"),
        ("scenario", "risk", "relates_to"),
        ("scenario", "portfolio", "relates_to"),
    ]

    for idx, (source, target, relation) in enumerate(relations, start=1):
        edge = KnowledgeEdge(
            id=f"edge-trading-{idx}",
            source_id=source,
            target_id=target,
            relation=relation,
            weight=1.0,
            confidence=0.8,
        )
        graph.add_edge(edge)
