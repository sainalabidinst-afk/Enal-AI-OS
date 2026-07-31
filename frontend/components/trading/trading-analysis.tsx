"use client";

import { useState, useCallback } from "react";
import { analyzeMarket } from "@/services/trading";
import { ConfidenceMeter } from "./confidence-meter";
import { EvidencePanel } from "./evidence-panel";
import type { TradingAnalysisResult } from "@/types/trading";
import { useToast } from "@/components/ui/toast";

export function TradingAnalysis() {
  const [symbol, setSymbol] = useState("BTCUSDT");
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<TradingAnalysisResult | null>(null);
  const { showError } = useToast();

  const handleAnalyze = useCallback(async () => {
    if (!symbol.trim()) return;

    setIsLoading(true);
    setResult(null);

    try {
      const response = await analyzeMarket(symbol.trim());
      if (response.success && response.data) {
        setResult(response.data);
      } else {
        showError(response.error || "Analysis failed");
      }
    } catch (error) {
      showError(
        "Failed to analyze market",
        error instanceof Error ? error.message : undefined
      );
    } finally {
      setIsLoading(false);
    }
  }, [symbol, showError]);

  const riskColor =
    result?.risk_level === "low" ? "text-green-500" :
    result?.risk_level === "high" ? "text-red-500" :
    "text-yellow-500";

  return (
    <div className="mx-auto max-w-4xl p-6 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-[var(--color-text-primary)]">
          Market Intelligence
        </h1>
        <p className="text-sm text-[var(--color-text-secondary)] mt-1">
          Multi-timeframe analysis with evidence and confidence scoring
        </p>
      </div>

      {/* Input */}
      <div className="flex gap-3">
        <input
          type="text"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value.toUpperCase())}
          onKeyDown={(e) => e.key === "Enter" && handleAnalyze()}
          placeholder="Enter symbol, e.g. BTCUSDT"
          className="flex-1 rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-secondary)] px-4 py-2 text-sm text-[var(--color-text-primary)] placeholder:text-[var(--color-text-secondary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-accent)]"
          disabled={isLoading}
        />
        <button
          onClick={handleAnalyze}
          disabled={isLoading || !symbol.trim()}
          className="rounded-lg bg-[var(--color-accent)] px-6 py-2 text-sm font-medium text-white hover:opacity-90 disabled:opacity-50"
        >
          {isLoading ? "Analyzing..." : "Analyze"}
        </button>
      </div>

      {/* Loading */}
      {isLoading && (
        <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-8 text-center animate-pulse">
          <p className="text-sm text-[var(--color-text-secondary)]">
            Fetching market data and computing indicators...
          </p>
        </div>
      )}

      {/* Results */}
      {result && (
        <div className="space-y-6">
          {/* Summary Card */}
          <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-6 space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-lg font-bold text-[var(--color-text-primary)]">
                  {result.symbol}
                </h2>
                <p className="text-xs text-[var(--color-text-secondary)]">
                  {result.metadata.exchange} &middot; {result.metadata.timeframes.join(", ")}
                </p>
              </div>
              <div className="text-right">
                <p className={`text-sm font-semibold ${riskColor}`}>
                  Risk: {result.risk_level.toUpperCase()}
                </p>
                <p className="text-[10px] text-[var(--color-text-secondary)]">
                  Latency: {result.metadata.latency_ms.toFixed(0)}ms
                </p>
              </div>
            </div>

            <ConfidenceMeter
              confidence={result.confidence}
              bias={result.bias}
              size="lg"
            />

            <p className="text-sm text-[var(--color-text-secondary)] leading-relaxed">
              {result.summary}
            </p>

            <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
              {Object.entries(result.raw.category_scores).map(([cat, score]) => (
                <div
                  key={cat}
                  className="rounded-lg bg-[var(--color-bg-tertiary)] p-2 text-center"
                >
                  <p className="text-[10px] text-[var(--color-text-secondary)] capitalize">
                    {cat.replace(/_/g, " ")}
                  </p>
                  <p className={`text-sm font-semibold ${
                    score > 0 ? "text-green-500" : score < 0 ? "text-red-500" : ""
                  }`}>
                    {score > 0 ? "+" : ""}{(score * 100).toFixed(0)}%
                  </p>
                </div>
              ))}
            </div>

            {/* Evidence Panel */}
            <EvidencePanel evidence={result.evidence} />

            {/* Strategy & Counter-scenario */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-4 space-y-2">
                <h3 className="text-sm font-semibold text-[var(--color-text-primary)]">
                  Suggested Strategy
                </h3>
                <p className="text-sm text-[var(--color-text-secondary)] leading-relaxed">
                  {result.suggested_strategy}
                </p>
              </div>
              <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-4 space-y-2">
                <h3 className="text-sm font-semibold text-[var(--color-text-primary)]">
                  Counter Scenario
                </h3>
                <p className="text-sm text-[var(--color-text-secondary)] leading-relaxed">
                  {result.counter_scenario}
                </p>
              </div>
            </div>

            {/* Reasoning Steps */}
            <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-4 space-y-2">
              <h3 className="text-sm font-semibold text-[var(--color-text-primary)]">
                Reasoning Trace
              </h3>
              <div className="space-y-1">
                {result.reasoning_steps.map((step, i) => (
                  <p key={i} className="text-xs text-[var(--color-text-secondary)]">
                    {step}
                  </p>
                ))}
              </div>
            </div>

            {/* Metadata */}
            <div className="text-[10px] text-[var(--color-text-secondary)] space-y-1">
              <p>Analysis version: {result.metadata.analysis_version}</p>
              <p>Generated at: {result.metadata.generated_at}</p>
              <p>Data source: {result.metadata.data_source}</p>
              <p>Raw data points: {result.metadata.raw_data_points}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
