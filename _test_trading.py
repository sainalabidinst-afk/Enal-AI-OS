#!/usr/bin/env python3
"""End-to-end test of the Trading Market Intelligence pipeline."""
import asyncio
from apps.trading_analyst.market_intelligence.provider import build_trading_context, DEFAULT_TIMEFRAMES
from apps.trading_analyst.market_intelligence.analyzer import MarketAnalyzer
from apps.trading_analyst.market_intelligence.summary import MarketSummaryGenerator


async def test():
    print("=" * 70)
    print("TRADING MARKET INTELLIGENCE - E2E TEST")
    print("=" * 70)
    
    symbol = "BTCUSDT"
    timeframes = ["15m", "1h", "4h", "1d"]
    
    print(f"\n1. Building trading context for {symbol}...")
    ctx = await build_trading_context(symbol, timeframes)
    print(f"   Timeframes fetched: {list(ctx.timeframes.keys())}")
    for tf, ohlcv in ctx.timeframes.items():
        first_close = ohlcv[0].close
        last_close = ohlcv[-1].close
        print(f"   {tf}: {len(ohlcv)} candles, close {first_close:.2f} -> {last_close:.2f}")
    
    print(f"\n2. Analyzing market...")
    analyzer = MarketAnalyzer()
    raw_evidence = await analyzer.analyze(ctx)
    analyzed = analyzer.get_analyzed_timeframes()
    print(f"   Analyzed timeframes: {analyzed}")
    total = sum(len(v) for v in raw_evidence.values())
    by_cat = {k: len(v) for k, v in raw_evidence.items()}
    print(f"   Raw evidence: {total} total, by category: {by_cat}")
    
    # Find first non-empty category for sampling
    sample = None
    for cat, ev_list in raw_evidence.items():
        if ev_list:
            sample = ev_list[0]
            break
    if sample:
        print(f"   Sample: id={sample.id}, type={sample.type}, desc={sample.description[:80]}")
    
    print(f"\n3. Generating summary...")
    generator = MarketSummaryGenerator()
    result = generator.generate(raw_evidence, analyzed, symbol, "binance", 150.0)
    
    print(f"   Bias: {result.bias}")
    print(f"   Confidence: {result.confidence}")
    print(f"   Risk: {result.risk_level}")
    print(f"   Evidence count: {len(result.evidence)}")
    print(f"   Summary: {result.summary[:120]}...")
    print(f"   Category scores: {result.raw['category_scores']}")
    
    print(f"\n4. Evidence details:")
    for ev in result.evidence[:5]:
        print(f"   - [{ev.type}] {ev.description[:80]} ({ev.timeframe}, dir={ev.direction}, str={ev.strength:.2f})")
    
    if len(result.evidence) > 5:
        print(f"   ... and {len(result.evidence) - 5} more")
    
    print(f"\n5. Reasoning steps:")
    for step in result.reasoning_steps:
        print(f"   - {step}")
    
    print(f"\n6. Metadata:")
    print(f"   Generated at: {result.metadata.generated_at}")
    print(f"   Latency: {result.metadata.latency_ms:.0f}ms")
    print(f"   Version: {result.metadata.analysis_version}")
    
    print(f"\n{'=' * 70}")
    print(f"  E2E TEST PASSED")
    print(f"  {symbol}: {result.bias.upper()} | Confidence: {result.confidence}% | Risk: {result.risk_level}")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    asyncio.run(test())
