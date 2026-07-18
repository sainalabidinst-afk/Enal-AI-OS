"use client";

import type { ExecutionSession, ExecutionPhase, ExecutionStatus } from "@/types/execution";
import { useState } from "react";
import { ApprovalDialog } from "@/components/ui/approval-dialog";

interface ExecutionTimelineProps {
  execution: ExecutionSession;
  onCancel?: () => Promise<void>;
  onRetry?: (goal: string) => void;
}

export function ExecutionTimeline({ execution, onCancel, onRetry }: ExecutionTimelineProps) {
  const [approvalOpen, setApprovalOpen] = useState(false);
  const [cancelling, setCancelling] = useState(false);

  const handleCancel = async () => {
    if (!onCancel) return;
    setCancelling(true);
    try {
      await onCancel();
      setApprovalOpen(false);
    } catch (err) {
      // handled by parent store
    } finally {
      setCancelling(false);
    }
  };

  const phases: ExecutionPhase[] = (execution.phases || []) as ExecutionPhase[];
  const runningCount = phases.filter((p) => p.status === "running").length;
  const isRunning = ["pending", "planning", "running", "waiting_approval", "paused"].includes(execution.status);

  return (
    <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-4 space-y-4">
      <div className="flex items-start justify-between">
        <div>
          <h3 className="text-sm font-semibold">Execution</h3>
          <p className="text-xs text-[var(--color-text-secondary)] mt-1 line-clamp-2">{execution.goal}</p>
        </div>
        <div className="flex items-center gap-2">
          {execution.status === "failed" && onRetry && (
            <button
              onClick={() => onRetry(execution.goal)}
              className="text-xs rounded-lg border border-[var(--color-accent)] px-3 py-1 text-[var(--color-accent)] hover:bg-[var(--color-accent)]/10"
            >
              Retry
            </button>
          )}
          {isRunning && onCancel && (
            <button
              onClick={() => setApprovalOpen(true)}
              disabled={cancelling}
              className="text-xs rounded-lg border border-[var(--color-danger)] px-3 py-1 text-[var(--color-danger)] hover:bg-[var(--color-danger)]/10 disabled:opacity-50"
            >
              Cancel
            </button>
          )}
        </div>
      </div>

      <div className="space-y-2">
        <div className="flex items-center justify-between text-xs">
          <span className="text-[var(--color-text-secondary)]">{execution.status}</span>
          <span className="font-mono">{Math.round(execution.progress || 0)}%</span>
        </div>
        <div className="h-2 rounded-full bg-[var(--color-bg-primary)]">
          <div
            className="h-2 rounded-full bg-[var(--color-accent)] transition-all"
            style={{ width: `${Math.min(100, Math.max(0, execution.progress || 0))}%` }}
          />
        </div>
        {execution.eta_seconds != null && (
          <p className="text-xs text-[var(--color-text-secondary)]">ETA: {Math.round(execution.eta_seconds / 60)} min</p>
        )}
      </div>

      {phases.length > 0 && (
        <div className="space-y-2">
          <p className="text-xs font-semibold uppercase tracking-wide text-[var(--color-text-secondary)]">Phases</p>
          <div className="space-y-1">
            {phases.map((phase) => {
              const typedPhase = phase as ExecutionPhase & Record<string, any>;
              return (
                <div key={typedPhase.id} className="flex items-center justify-between rounded-md border border-[var(--color-border)] bg-[var(--color-bg-primary)] px-3 py-2">
                  <div className="flex items-center gap-2">
                    <PhaseIndicator status={typedPhase.status} />
                    <span className="text-sm">{typedPhase.name}</span>
                  </div>
                  <span className="text-xs text-[var(--color-text-secondary)]">{typedPhase.status}</span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {execution.error && (
        <div className="rounded-md border border-[var(--color-danger)] bg-[var(--color-bg-primary)] px-4 py-3 text-sm text-[var(--color-danger)]">
          {execution.error}
        </div>
      )}

      <ApprovalDialog
        open={approvalOpen}
        title="Cancel execution"
        description="This will stop the current execution. This action cannot be undone."
        reason="User requested cancellation"
        impact="Running tasks will be interrupted. Partial results may be retained."
        confirmLabel="Cancel execution"
        danger
        onConfirm={handleCancel}
        onCancel={() => setApprovalOpen(false)}
      />
    </div>
  );
}

function PhaseIndicator({ status }: { status: ExecutionStatus }) {
  const colorMap: Record<ExecutionStatus, string> = {
    pending: "bg-[var(--color-text-secondary)]",
    planning: "bg-[var(--color-warning)]",
    running: "bg-[var(--color-accent)]",
    waiting_approval: "bg-[var(--color-warning)]",
    paused: "bg-[var(--color-warning)]",
    completed: "bg-[var(--color-success)]",
    failed: "bg-[var(--color-danger)]",
    cancelled: "bg-[var(--color-text-secondary)]",
  };

  return <span className={`inline-block h-2 w-2 rounded-full ${colorMap[status] || "bg-[var(--color-text-secondary)]"}`} />;
}
