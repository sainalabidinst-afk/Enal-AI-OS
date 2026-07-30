"use client";

import { useState } from "react";
import { analyzeTradingWithKnowledge } from "@/services/integration";
import type { IntegrationResult } from "@/types/integration";

export function TradingAnalysisIntegration() {
  const [symbol, setSymbol] = useState("BTCUSDT");
  const [timeframes, setTimeframes] = useState("15m,1h,4h,1d");
  const [exchange, setExchange] = useState("binance");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<IntegrationResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await analyzeTradingWithKnowledge({
        symbol,
        timeframes: timeframes.split(",").map((t) => t.trim()),
        exchange,
      });

      if (response.success && response.data) {
        setResult(response.data);
      } else {
        setError(response.error || "Analysis failed");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
          <div>
            <label className="block text-sm font-medium text-[var(--color-text-primary)]">
              Symbol
            </label>
            <input
              type="text"
              value={symbol}
              onChange={(e) => setSymbol(e.target.value.toUpperCase())}
              className="mt-1 block w-full rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] px-3 py-2 text-sm text-[var(--color-text-primary)]"
              placeholder="BTCUSDT"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-[var(--color-text-primary)]">
              Timeframes (comma-separated)
            </label>
            <input
              type="text"
              value={timeframes}
              onChange={(e) => setTimeframes(e.target.value)}
              className="mt-1 block w-full rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] px-3 py-2 text-sm text-[var(--color-text-primary)]"
              placeholder="15m,1h,4h,1d"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-[var(--color-text-primary)]">
              Exchange
            </label>
            <input
              type="text"
              value={exchange}
              onChange={(e) => setExchange(e.target.value)}
              className="mt-1 block w-full rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] px-3 py-2 text-sm text-[var(--color-text-primary)]"
              placeholder="binance"
            />
          </div>
        </div>
        <button
          type="submit"
          disabled={loading}
          className="rounded-lg bg-[var(--color-accent)] px-4 py-2 text-sm font-medium text-white hover:opacity-90 disabled:opacity-50 transition-opacity"
        >
          {loading ? "Analyzing..." : "Run Integrated Analysis"}
        </button>
      </form>

      {error && (
        <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-800 dark:border-red-800 dark:bg-red-950 dark:text-red-200">
          {error}
        </div>
      )}

      {result && (
        <div className="space-y-4">
          <IntegrationResultView result={result} />
        </div>
      )}
    </div>
  );
}

function IntegrationResultView({ result }: { result: IntegrationResult }) {
  return (
    <div className="space-y-4">
      <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] p-4">
        <h3 className="text-lg font-semibold text-[var(--color-text-primary)]">
          Integration Result
        </h3>
        <div className="mt-2 grid grid-cols-2 gap-4 text-sm">
          <div>
            <span className="text-[var(--color-text-secondary)]">Workflow ID:</span>
            <span className="ml-2 font-mono text-[var(--color-text-primary)]">
              {result.workflow_id}
            </span>
          </div>
          <div>
            <span className="text-[var(--color-text-secondary)]">Latency:</span>
            <span className="ml-2 text-[var(--color-text-primary)]">
              {result.latency_ms.toFixed(1)}ms
            </span>
          </div>
        </div>
      </div>

      {result.reasoning_chain.length > 0 && (
        <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] p-4">
          <h4 className="text-sm font-semibold text-[var(--color-text-primary)]">
            Reasoning Chain
          </h4>
          <ol className="mt-2 list-inside list-decimal space-y-1 text-sm text-[var(--color-text-secondary)]">
            {result.reasoning_chain.map((step, idx) => (
              <li key={idx}>{step}</li>
            ))}
          </ol>
        </div>
      )}

      {result.evidences.length > 0 && (
        <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] p-4">
          <h4 className="text-sm font-semibold text-[var(--color-text-primary)]">
            Unified Evidence ({result.evidences.length})
          </h4>
          <div className="mt-2 space-y-2">
            {result.evidences.slice(0, 10).map((ev) => (
              <div
                key={ev.id}
                className="rounded border border-[var(--color-border)] p-2 text-xs"
              >
                <div className="flex items-center justify-between">
                  <span className="font-mono text-[var(--color-text-primary)]">
                    {ev.id}
                  </span>
                  <span className="text-[var(--color-text-secondary)]">
                    {ev.source} · {ev.type}
                  </span>
                </div>
                <p className="mt-1 text-[var(--color-text-secondary)]">
                  {ev.content}
                </p>
                <div className="mt-1 flex gap-3 text-[var(--color-text-secondary)]">
                  <span>conf: {ev.confidence.toFixed(2)}</span>
                  {ev.strength > 0 && <span>str: {ev.strength.toFixed(2)}</span>}
                  {ev.direction && <span>dir: {ev.direction}</span>}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {result.knowledge_updates.length > 0 && (
        <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] p-4">
          <h4 className="text-sm font-semibold text-[var(--color-text-primary)]">
            Knowledge Updates
          </h4>
          <div className="mt-2 space-y-1">
            {result.knowledge_updates.map((update, idx) => (
              <div
                key={idx}
                className="flex items-center justify-between text-xs"
              >
                <span className="font-mono text-[var(--color-text-primary)]">
                  {update.entity_id}
                </span>
                <span className="text-[var(--color-text-secondary)]">
                  {update.action} · {update.domain}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
