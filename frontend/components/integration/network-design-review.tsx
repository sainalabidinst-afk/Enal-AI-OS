"use client";

import { useState } from "react";
import { reviewNetworkDesignWithKnowledge } from "@/services/integration";
import type { IntegrationResult } from "@/types/integration";

export function NetworkDesignReviewIntegration() {
  const [topology, setTopology] = useState(
    "3-tier datacenter with core, distribution, and access layers. Redundant uplinks between core and distribution switches."
  );
  const [requirements, setRequirements] = useState(
    "Support 500 branches with zero-trust security and SD-WAN capability."
  );
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<IntegrationResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await reviewNetworkDesignWithKnowledge({
        topology_description: topology,
        requirements,
      });

      if (response.success && response.data) {
        setResult(response.data);
      } else {
        setError(response.error || "Review failed");
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
        <div>
          <label className="block text-sm font-medium text-[var(--color-text-primary)]">
            Topology Description
          </label>
          <textarea
            value={topology}
            onChange={(e) => setTopology(e.target.value)}
            rows={4}
            className="mt-1 block w-full rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] px-3 py-2 text-sm text-[var(--color-text-primary)]"
            placeholder="Describe your network topology..."
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-[var(--color-text-primary)]">
            Requirements
          </label>
          <textarea
            value={requirements}
            onChange={(e) => setRequirements(e.target.value)}
            rows={3}
            className="mt-1 block w-full rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] px-3 py-2 text-sm text-[var(--color-text-primary)]"
            placeholder="Describe network requirements..."
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="rounded-lg bg-[var(--color-accent)] px-4 py-2 text-sm font-medium text-white hover:opacity-90 disabled:opacity-50 transition-opacity"
        >
          {loading ? "Reviewing..." : "Run Design Review"}
        </button>
      </form>

      {error && (
        <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-800 dark:border-red-800 dark:bg-red-950 dark:text-red-200">
          {error}
        </div>
      )}

      {result && <IntegrationResultView result={result} />}
    </div>
  );
}

function IntegrationResultView({ result }: { result: IntegrationResult }) {
  return (
    <div className="space-y-4">
      <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] p-4">
        <h3 className="text-lg font-semibold text-[var(--color-text-primary)]">
          Design Review Result
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
            Knowledge Context ({result.evidences.length} items)
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
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
