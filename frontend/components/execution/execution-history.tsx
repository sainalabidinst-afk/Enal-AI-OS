"use client";

import type { ExecutionSession } from "@/types/execution";
import { useState } from "react";
import { useExecutionStore } from "@/store/execution-store";
import { ExecutionTimeline } from "./execution-timeline";

interface ExecutionHistoryPanelProps {
  selectedExecutionId?: string | null;
  onSelectExecution: (id: string) => void;
}

export function ExecutionHistoryPanel({ selectedExecutionId, onSelectExecution }: ExecutionHistoryPanelProps) {
  const executions = useExecutionStore((s) => s.executions);
  const cancelExecution = useExecutionStore((s) => s.cancelExecution);

  const list = Object.values(executions).sort((a, b) => (b.created_at > a.created_at ? 1 : -1));

  return (
    <div className="space-y-4">
      {list.length === 0 && (
        <p className="text-sm text-[var(--color-text-secondary)]">No executions yet.</p>
      )}
      {list.map((execution) => (
        <button
          key={execution.id}
          onClick={() => onSelectExecution(execution.id)}
          className={`w-full text-left rounded-lg border p-4 transition-colors ${
            selectedExecutionId === execution.id
              ? "border-[var(--color-accent)] bg-[var(--color-bg-secondary)]"
              : "border-[var(--color-border)] bg-[var(--color-bg-secondary)] hover:border-[var(--color-text-secondary)]"
          }`}
        >
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <p className="text-sm font-medium">{execution.goal}</p>
              <p className="text-xs text-[var(--color-text-secondary)] mt-1">
                {new Date(execution.created_at).toLocaleString()} • {execution.status}
              </p>
            </div>
            <StatusBadge status={execution.status} />
          </div>
        </button>
      ))}

      {selectedExecutionId && (
        <ExecutionDetail
          executionId={selectedExecutionId}
          onClose={() => onSelectExecution("")}
          onCancel={cancelExecution}
        />
      )}
    </div>
  );
}

function ExecutionDetail({
  executionId,
  onCancel,
  onClose,
}: {
  executionId: string;
  onCancel: (id: string) => Promise<void>;
  onClose: () => void;
}) {
  const execution = useExecutionStore((s) => s.executions[executionId]);
  const refreshExecution = useExecutionStore((s) => s.refreshExecution);
  const loadLogs = useExecutionStore((s) => s.loadLogs);
  const logs = useExecutionStore((s) => s.logs);
  const [showLogs, setShowLogs] = useState(false);

  if (!execution) {
    refreshExecution(executionId);
    return <div className="text-sm text-[var(--color-text-secondary)]">Loading execution...</div>;
  }

  return (
    <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold">Execution Detail</h3>
        <button onClick={onClose} className="text-xs text-[var(--color-text-secondary)] hover:underline">
          Close
        </button>
      </div>
      <div className="mt-4">
        <ExecutionTimeline
          execution={execution}
          onCancel={() => onCancel(executionId)}
        />
      </div>
      <div className="mt-4">
        <button onClick={() => { setShowLogs(!showLogs); loadLogs(executionId); }} className="text-xs text-[var(--color-text-secondary)] hover:underline">
          {showLogs ? "Hide logs" : "Show logs"}
        </button>
        {showLogs && logs.length > 0 && (
          <div className="mt-2 rounded-md border border-[var(--color-border)] bg-[var(--color-bg-primary)] p-3 space-y-1 max-h-60 overflow-y-auto">
            {logs.map((log, idx) => (
              <div key={idx} className="text-xs">
                <span className="text-[var(--color-text-secondary)]">[{log.level || "info"}]</span> {log.message}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const colorMap: Record<string, string> = {
    pending: "bg-[var(--color-text-secondary)]/20 text-[var(--color-text-secondary)]",
    planning: "bg-[var(--color-warning)]/20 text-[var(--color-warning)]",
    running: "bg-[var(--color-accent)]/20 text-[var(--color-accent)]",
    waiting_approval: "bg-[var(--color-warning)]/20 text-[var(--color-warning)]",
    paused: "bg-[var(--color-warning)]/20 text-[var(--color-warning)]",
    completed: "bg-[var(--color-success)]/20 text-[var(--color-success)]",
    failed: "bg-[var(--color-danger)]/20 text-[var(--color-danger)]",
    cancelled: "bg-[var(--color-text-secondary)]/20 text-[var(--color-text-secondary)]",
  };

  return (
    <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${colorMap[status] || colorMap.pending}`}>
      {status}
    </span>
  );
}
