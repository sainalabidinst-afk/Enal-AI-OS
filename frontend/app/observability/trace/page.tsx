"use client";

import { useEffect, useState } from "react";
import { getTrace, type TraceSpan } from "@/services/observability";
import { ErrorBoundary } from "@/components/ui/error-boundary";
import { useParams, useRouter } from "next/navigation";

function TracePageContent() {
  const router = useRouter();
  const params = useParams<{ traceId?: string }>();
  const traceId = params?.traceId;
  const [spans, setSpans] = useState<TraceSpan[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [inputId, setInputId] = useState("");

  const handleFetch = async (id: string) => {
    if (!id.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const data = await getTrace(id.trim());
      setSpans(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load trace");
      setSpans([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (traceId) {
      void handleFetch(traceId);
    }
  }, [traceId]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputId.trim()) {
      router.push(`/observability/trace/${encodeURIComponent(inputId.trim())}`);
    }
  };

  const totalDuration = spans.reduce((sum, s) => sum + (s.latency_ms || 0), 0);

  return (
    <div className="mx-auto max-w-5xl p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-[var(--color-text-primary)]">Trace Viewer</h1>
        <p className="text-sm text-[var(--color-text-secondary)] mt-1">
          View distributed trace spans from observability data.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="flex gap-3">
        <input
          type="text"
          value={inputId}
          onChange={(e) => setInputId(e.target.value)}
          placeholder="Enter trace ID..."
          className="flex-1 rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] px-3 py-2 text-sm text-[var(--color-text-primary)] focus:border-[var(--color-accent)] focus:outline-none"
        />
        <button
          type="submit"
          disabled={!inputId.trim() || loading}
          className="rounded-lg bg-[var(--color-accent)] px-4 py-2 text-sm font-medium text-white hover:opacity-90 disabled:opacity-50"
        >
          {loading ? "Loading..." : "Fetch Trace"}
        </button>
      </form>

      {error && (
        <div className="rounded-lg border border-[var(--color-danger)] bg-red-900/20 px-4 py-2.5 text-sm text-[var(--color-danger)]">
          {error}
        </div>
      )}

      {!spans.length && !loading && !error && (
        <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-5">
          <p className="text-xs text-[var(--color-text-secondary)]">
            Enter a trace ID above or navigate via a trace link to view spans.
          </p>
        </div>
      )}

      {spans.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-[var(--color-text-primary)]">
              Trace: {spans[0].trace_id}
            </h2>
            <span className="text-xs text-[var(--color-text-secondary)]">
              {spans.length} spans · {totalDuration.toFixed(0)}ms total latency
            </span>
          </div>

          <div className="overflow-x-auto rounded-lg border border-[var(--color-border)]">
            <table className="w-full text-xs">
              <thead>
                <tr className="border-b border-[var(--color-border)] bg-[var(--color-bg-secondary)]">
                  <th className="px-3 py-2 text-left font-medium text-[var(--color-text-secondary)] uppercase">
                    Name
                  </th>
                  <th className="px-3 py-2 text-left font-medium text-[var(--color-text-secondary)] uppercase">
                    Type
                  </th>
                  <th className="px-3 py-2 text-left font-medium text-[var(--color-text-secondary)] uppercase">
                    Agent
                  </th>
                  <th className="px-3 py-2 text-right font-medium text-[var(--color-text-secondary)] uppercase">
                    Latency (ms)
                  </th>
                  <th className="px-3 py-2 text-right font-medium text-[var(--color-text-secondary)] uppercase">
                    Tokens
                  </th>
                  <th className="px-3 py-2 text-right font-medium text-[var(--color-text-secondary)] uppercase">
                    Cost
                  </th>
                  <th className="px-3 py-2 text-center font-medium text-[var(--color-text-secondary)] uppercase">
                    Status
                  </th>
                </tr>
              </thead>
              <tbody>
                {spans.map((span) => (
                  <tr key={span.id} className="border-b border-[var(--color-border)]">
                    <td className="px-3 py-2 text-[var(--color-text-primary)]">{span.name}</td>
                    <td className="px-3 py-2 text-[var(--color-text-secondary)]">{span.type}</td>
                    <td className="px-3 py-2 text-[var(--color-text-secondary)]">{span.agent || "—"}</td>
                    <td className="px-3 py-2 text-right font-mono">{span.latency_ms.toFixed(1)}</td>
                    <td className="px-3 py-2 text-right font-mono">{span.tokens || 0}</td>
                    <td className="px-3 py-2 text-right font-mono">{span.cost.toFixed(4)}</td>
                    <td className="px-3 py-2 text-center">
                      <span
                        className={
                          span.success
                            ? "inline-block h-2 w-2 rounded-full bg-green-400"
                            : "inline-block h-2 w-2 rounded-full bg-red-400"
                        }
                        title={span.error || ""}
                      />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

export default function TracePage() {
  return (
    <ErrorBoundary>
      <TracePageContent />
    </ErrorBoundary>
  );
}
