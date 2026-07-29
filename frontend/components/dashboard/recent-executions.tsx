"use client";

import type { ExecutionSession } from "@/types/execution";

const statusColors: Record<string, string> = {
  pending: "text-yellow-400",
  planning: "text-blue-400",
  running: "text-blue-400",
  completed: "text-green-400",
  failed: "text-red-400",
  cancelled: "text-gray-400",
  paused: "text-yellow-400",
  waiting_approval: "text-orange-400",
};

const statusLabels: Record<string, string> = {
  pending: "Pending",
  planning: "Planning",
  running: "Running",
  completed: "Completed",
  failed: "Failed",
  cancelled: "Cancelled",
  paused: "Paused",
  waiting_approval: "Awaiting Approval",
};

interface RecentExecutionsProps {
  executions: ExecutionSession[];
  isLoading: boolean;
  onSelect: (id: string) => void;
}

function formatDuration(createdAt: string, completedAt?: string): string {
  const start = new Date(createdAt).getTime();
  const end = completedAt ? new Date(completedAt).getTime() : Date.now();
  const diffMs = end - start;
  const seconds = Math.floor(diffMs / 1000);

  if (seconds < 60) return `${seconds}s`;
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m ${seconds % 60}s`;
  const hours = Math.floor(minutes / 60);
  return `${hours}h ${minutes % 60}m`;
}

function formatTime(iso: string): string {
  const date = new Date(iso);
  return date.toLocaleString(undefined, {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function RecentExecutions({ executions, isLoading, onSelect }: RecentExecutionsProps) {
  if (isLoading) {
    return (
      <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-4 animate-pulse space-y-3">
        <div className="h-4 w-32 bg-[var(--color-bg-tertiary)] rounded mb-4" />
        {Array.from({ length: 4 }).map((_, i) => (
          <div key={i} className="h-12 bg-[var(--color-bg-tertiary)] rounded" />
        ))}
      </div>
    );
  }

  const recent = [...executions]
    .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
    .slice(0, 10);

  return (
    <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-4">
      <h2 className="text-sm font-semibold text-[var(--color-text-primary)] mb-4">
        Recent Executions
      </h2>

      {recent.length === 0 ? (
        <div className="text-center py-8">
          <p className="text-sm text-[var(--color-text-secondary)]">
            No executions yet. Start one from the{" "}
            <a href="/executions" className="text-[var(--color-accent)] hover:underline">
              Executions page
            </a>
            .
          </p>
        </div>
      ) : (
        <div className="space-y-1">
          {recent.map((exec) => (
            <button
              key={exec.id}
              onClick={() => onSelect(exec.id)}
              className="w-full flex items-center gap-3 rounded-lg px-3 py-2 text-left hover:bg-[var(--color-bg-tertiary)] transition-colors"
            >
              {/* Status dot */}
              <span
                className={`h-2 w-2 rounded-full flex-shrink-0 ${
                  statusColors[exec.status] || "text-gray-400"
                }`}
                style={{ backgroundColor: "currentColor" }}
              />

              {/* Goal */}
              <div className="flex-1 min-w-0">
                <p className="text-sm text-[var(--color-text-primary)] truncate">
                  {exec.goal}
                </p>
                <p className="text-xs text-[var(--color-text-secondary)]">
                  {formatTime(exec.created_at)} · {formatDuration(exec.created_at, exec.completed_at)}
                </p>
              </div>

              {/* Status badge */}
              <span
                className={`text-xs font-medium px-2 py-0.5 rounded-full flex-shrink-0 ${
                  statusColors[exec.status]
                } bg-current/10`}
                style={{
                  color: statusColors[exec.status],
                  backgroundColor: `${statusColors[exec.status]}15`,
                }}
              >
                {statusLabels[exec.status] || exec.status}
              </span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

