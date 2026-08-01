"use client";

import { useState } from "react";
import { runSelfImprovementCycle } from "@/services/integration";
import type { IntegrationResult } from "@/types/integration";

export function SelfImprovementIntegration() {
  const [projectPath, setProjectPath] = useState("/path/to/project");
  const [analysisType, setAnalysisType] = useState("full");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<IntegrationResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await runSelfImprovementCycle({
        project_path: projectPath,
        analysis_type: analysisType,
      });

      if (response.success && response.data) {
        setResult(response.data);
      } else {
        setError(response.error || "Self-improvement cycle failed");
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
            Project Path
          </label>
          <input
            type="text"
            value={projectPath}
            onChange={(e) => setProjectPath(e.target.value)}
            className="mt-1 block w-full rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] px-3 py-2 text-sm text-[var(--color-text-primary)]"
            placeholder="/path/to/project"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-[var(--color-text-primary)]">
            Analysis Type
          </label>
          <select
            value={analysisType}
            onChange={(e) => setAnalysisType(e.target.value)}
            className="mt-1 block w-full rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] px-3 py-2 text-sm text-[var(--color-text-primary)]"
          >
            <option value="full">Full Analysis</option>
            <option value="security">Security</option>
            <option value="performance">Performance</option>
            <option value="architecture">Architecture</option>
          </select>
        </div>
        <button
          type="submit"
          disabled={loading}
          className="rounded-lg bg-[var(--color-accent)] px-4 py-2 text-sm font-medium text-white hover:opacity-90 disabled:opacity-50 transition-opacity"
        >
          {loading ? "Running..." : "Run Self-Improvement Cycle"}
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
  // Backend result shape: { inputs, outputs, intermediate, reasoning_output, knowledge_context }
  const resultData = result.result as Record<string, unknown>;
  const outputs = resultData.outputs as Record<string, unknown> | undefined;
  const intermediate = resultData.intermediate as Record<string, unknown> | undefined;
  const reasoningOutput = resultData.reasoning_output as Record<string, unknown> | undefined;
  const knowledgeContext = resultData.knowledge_context as Record<string, unknown> | undefined;

  return (
    <div className="space-y-4">
      <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] p-4">
        <h3 className="text-lg font-semibold text-[var(--color-text-primary)]">
          Self-Improvement Result
        </h3>
        <div className="mt-2 grid grid-cols-2 gap-4 text-sm">
          <div>
            <span className="text-[var(--color-text-secondary)]">Workflow ID:</span>
            <span className="ml-2 font-mono text-[var(--color-text-primary)]">
              {result.workflow_id}
            </span>
          </div>
          <div>
            <span className="text-[var(--color-text-secondary)]">Workflow Type:</span>
            <span className="ml-2 text-[var(--color-text-primary)]">
              {result.workflow_type}
            </span>
          </div>
          <div>
            <span className="text-[var(--color-text-secondary)]">Status:</span>
            <span className="ml-2 text-[var(--color-text-primary)]">
              {result.success ? "Success" : "Failed"}
            </span>
          </div>
          <div>
            <span className="text-[var(--color-text-secondary)]">Latency:</span>
            <span className="ml-2 font-mono text-[var(--color-text-primary)]">
              {result.latency_ms}ms
            </span>
          </div>
        </div>
      </div>

      {outputs && Object.keys(outputs).length > 0 && (
        <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] p-4">
          <h4 className="text-sm font-semibold text-[var(--color-text-primary)]">
            Outputs
          </h4>
          <pre className="mt-2 overflow-auto text-xs text-[var(--color-text-secondary)]">
            {JSON.stringify(outputs, null, 2)}
          </pre>
        </div>
      )}

      {reasoningOutput && Object.keys(reasoningOutput).length > 0 && (
        <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] p-4">
          <h4 className="text-sm font-semibold text-[var(--color-text-primary)]">
            Reasoning
          </h4>
          <pre className="mt-2 overflow-auto text-xs text-[var(--color-text-secondary)]">
            {JSON.stringify(reasoningOutput, null, 2)}
          </pre>
        </div>
      )}

      {knowledgeContext && Object.keys(knowledgeContext).length > 0 && (
        <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] p-4">
          <h4 className="text-sm font-semibold text-[var(--color-text-primary)]">
            Knowledge Context
          </h4>
          <pre className="mt-2 overflow-auto text-xs text-[var(--color-text-secondary)]">
            {JSON.stringify(knowledgeContext, null, 2)}
          </pre>
        </div>
      )}

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

      {intermediate && Object.keys(intermediate).length > 0 && (
        <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] p-4">
          <h4 className="text-sm font-semibold text-[var(--color-text-primary)]">
            Intermediate Data
          </h4>
          <pre className="mt-2 overflow-auto text-xs text-[var(--color-text-secondary)]">
            {JSON.stringify(intermediate, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
