"use client";

import { useEffect, useState } from "react";
import { useExecutionStore } from "@/store/execution-store";
import { ErrorBoundary } from "@/components/ui/error-boundary";
import type { ExecutionSession } from "@/types/execution";

function LogsPageContent() {
  const executions = useExecutionStore((s) => s.executions);
  const loadExecutions = useExecutionStore((s) => s.loadExecutions);
  const loadLogs = useExecutionStore((s) => s.loadLogs);
  const activeExecutionId = useExecutionStore((s) => s.activeExecutionId);
  const setActiveExecution = useExecutionStore((s) => s.setActiveExecution);
  const logs = useExecutionStore((s) => s.logs);
  const isLoading = useExecutionStore((s) => s.isLoading);
  const error = useExecutionStore((s) => s.error);

  const [executionsList, setExecutionsList] = useState<ExecutionSession[]>([]);

  useEffect(() => {
    void loadExecutions();
  }, [loadExecutions]);

  useEffect(() => {
    const list = Object.values(executions);
    setExecutionsList(list);
    if (list.length > 0 && !activeExecutionId) {
      const latest = list[list.length - 1];
      setActiveExecution(latest.id);
    }
  }, [executions, activeExecutionId, setActiveExecution]);

  useEffect(() => {
    if (activeExecutionId) {
      void loadLogs(activeExecutionId);
    }
  }, [activeExecutionId, loadLogs]);

  const activeExecution = activeExecutionId ? executions[activeExecutionId] : undefined;

  return (
    <div className="mx-auto max-w-5xl p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-[var(--color-text-primary)]">System Logs</h1>
        <p className="text-sm text-[var(--color-text-secondary)] mt-1">
          View execution logs and system activity.
        </p>
      </div>

      {error && (
        <div className="rounded-lg border border-[var(--color-danger)] bg-red-900/20 px-4 py-2.5 text-sm text-[var(--color-danger)]">
          {error}
        </div>
      )}

      {executionsList.length === 0 && !isLoading && (
        <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-5">
          <p className="text-xs text-[var(--color-text-secondary)]">No executions recorded yet.</p>
        </div>
      )}

      {executionsList.length > 0 && (
        <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-3">
          <select
            value={activeExecutionId || ""}
            onChange={(e) => setActiveExecution(e.target.value)}
            className="w-full rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] px-3 py-2 text-sm text-[var(--color-text-primary)] focus:border-[var(--color-accent)] focus:outline-none"
          >
            {executionsList.map((exec) => (
              <option key={exec.id} value={exec.id}>
                {exec.id} — {exec.goal} ({exec.status})
              </option>
            ))}
          </select>
        </div>
      )}

      {activeExecution && (
        <div className="space-y-3">
          <div>
            <span className="text-xs font-medium text-[var(--color-text-secondary)]">Goal:</span>{" "}
            <span className="text-sm text-[var(--color-text-primary)]">{activeExecution.goal}</span>
          </div>
          <div>
            <span className="text-xs font-medium text-[var(--color-text-secondary)]">Status:</span>{" "}
            <span className="text-sm text-[var(--color-text-primary)] capitalize">
              {activeExecution.status}
            </span>
          </div>
        </div>
      )}

      <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] overflow-hidden">
        {logs.length > 0 ? (
          <div className="font-mono text-xs">
            <div className="border-b border-[var(--color-border)] px-3 py-2 bg-[var(--color-bg-secondary)]">
              <span className="text-[var(--color-text-secondary)]">Timestamp</span>
              <span className="ml-4 text-[var(--color-text-secondary)]">Level</span>
              <span className="ml-4 text-[var(--color-text-secondary)]">Message</span>
            </div>
            <div className="max-h-96 overflow-y-auto">
              {logs.map((log, i) => (
                <div key={i} className="border-b border-[var(--color-border)] px-3 py-1.5">
                  <span className="text-[var(--color-text-tertiary)] w-32 inline-block">
                    {log.timestamp || log.created_at || new Date().toISOString()}
                  </span>
                  <span
                    className={`ml-4 inline-block w-16 ${
                      log.level === "error"
                        ? "text-red-400"
                        : log.level === "warning"
                          ? "text-yellow-400"
                          : "text-green-400"
                    }`}
                  >
                    {(log.level || "info").toUpperCase()}
                  </span>
                  <span className="ml-4 text-[var(--color-text-primary)]">{log.message || JSON.stringify(log)}</span>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <div className="px-3 py-4 text-center text-xs text-[var(--color-text-secondary)]">
            {activeExecutionId ? "No logs for this execution." : "Select an execution to view logs."}
          </div>
        )}
      </div>
    </div>
  );
}

export default function LogsPage() {
  return (
    <ErrorBoundary>
      <LogsPageContent />
    </ErrorBoundary>
  );
}
