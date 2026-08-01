"use client";

import { useEffect, useState, useCallback, Suspense } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { useExecutionStore } from "@/store/execution-store";
import { useWorkspaceStore } from "@/store/workspace-store";
import { ExecutionHistoryPanel } from "@/components/execution/execution-history";
import { ExecutionTimeline } from "@/components/execution/execution-timeline";
import { ExecutionForm } from "@/components/execution/execution-form";
import { ListSkeleton, PageSkeleton } from "@/components/ui/loading-skeleton";
import { useToast } from "@/components/ui/toast";
import type { ExecutionSession } from "@/types/execution";

function ExecutionsPageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const selectedId = searchParams.get("selected");

  const [goal, setGoal] = useState("");
  const [showNewForm, setShowNewForm] = useState(false);

  const executions = useExecutionStore((s) => s.executions);
  const loadExecutions = useExecutionStore((s) => s.loadExecutions);
  const refreshExecution = useExecutionStore((s) => s.refreshExecution);
  const cancelExecution = useExecutionStore((s) => s.cancelExecution);
  const startExecution = useExecutionStore((s) => s.startExecution);
  const isLoading = useExecutionStore((s) => s.isLoading);
  const workspaces = useWorkspaceStore((s) => s.workspaces);
  const loadWorkspaces = useWorkspaceStore((s) => s.loadWorkspaces);
  const { showSuccess, showError, showInfo } = useToast();

  const selectedExecution = selectedId ? executions[selectedId] : null;

  // Load data on mount
  useEffect(() => {
    loadExecutions().catch(() => {});
    if (workspaces.length === 0) {
      loadWorkspaces().catch(() => {});
    }
  }, [loadExecutions, loadWorkspaces, workspaces.length]);

  // Auto-refresh for running executions
  useEffect(() => {
    if (!selectedExecution) return;
    const isRunning = ["pending", "planning", "running", "waiting_approval"].includes(
      selectedExecution.status
    );
    if (!isRunning) return;

    const interval = setInterval(() => {
      refreshExecution(selectedExecution.id);
    }, 3000);

    return () => clearInterval(interval);
  }, [selectedExecution?.id, selectedExecution?.status, refreshExecution]);

  const handleStartExecution = useCallback(async (goalText: string) => {
    const wsId = workspaces[0]?.id;
    if (!wsId) {
      showError("Workspace Required", "Please create a workspace first.");
      return;
    }
    try {
      const execution = await startExecution(goalText, wsId);
      if (execution) {
        showSuccess("Execution Started", goalText.slice(0, 80));
        router.push(`/executions?selected=${execution.id}`);
      }
    } catch (err) {
      showError("Failed to start", err instanceof Error ? err.message : "Unknown error");
    }
  }, [workspaces, startExecution, showError, showSuccess, router]);

  const handleRetry = useCallback(async (goalText: string) => {
    const wsId = workspaces[0]?.id;
    if (!wsId) return;
    try {
      const execution = await startExecution(goalText, wsId);
      if (execution) {
        showInfo("Retrying execution", goalText.slice(0, 80));
        router.push(`/executions?selected=${execution.id}`);
      }
    } catch (err) {
      showError("Retry failed", err instanceof Error ? err.message : "Unknown error");
    }
  }, [workspaces, startExecution, showError, showInfo, router]);

  const handleCancel = useCallback(async (executionId: string) => {
    try {
      await cancelExecution(executionId);
      showInfo("Execution cancelled");
    } catch {
      showError("Failed to cancel execution");
    }
  }, [cancelExecution, showError, showInfo]);

  const handleDeselect = useCallback(() => {
    router.push("/executions");
  }, [router]);

  const list = Object.values(executions).sort(
    (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
  );

  return (
    <div className="mx-auto max-w-5xl p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-[var(--color-text-primary)]">
            Executions
          </h1>
          <p className="text-sm text-[var(--color-text-secondary)] mt-1">
            Monitor and manage execution sessions
          </p>
        </div>
        <button
          onClick={() => setShowNewForm(true)}
          className="rounded-lg bg-[var(--color-accent)] px-4 py-2 text-sm font-medium text-white hover:opacity-90 transition-opacity"
        >
          + New Execution
        </button>
      </div>

      {/* Quick start form */}
      <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-4">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            if (goal.trim()) {
              handleStartExecution(goal.trim());
              setGoal("");
            }
          }}
          className="flex gap-2"
        >
          <input
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            placeholder="Enter a goal to execute..."
            className="flex-1 rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] px-4 py-2.5 text-sm text-[var(--color-text-primary)] placeholder:text-[var(--color-text-secondary)] focus:border-[var(--color-accent)] focus:outline-none focus:ring-1 focus:ring-[var(--color-accent)]"
          />
          <button
            type="submit"
            disabled={!goal.trim()}
            className="rounded-lg bg-[var(--color-accent)] px-5 py-2.5 text-sm font-medium text-white hover:opacity-90 disabled:opacity-50 transition-opacity"
          >
            Run
          </button>
        </form>
      </div>

      {/* Main content: split view when execution selected */}
      <div className={`grid gap-6 ${selectedExecution ? "grid-cols-1 lg:grid-cols-5" : "grid-cols-1"}`}>
        {/* Left: execution list */}
        <div className={selectedExecution ? "lg:col-span-2" : ""}>
          <h2 className="text-sm font-semibold text-[var(--color-text-primary)] mb-3">
            {isLoading ? "Loading..." : `${list.length} Execution${list.length !== 1 ? "s" : ""}`}
          </h2>
          {isLoading && list.length === 0 ? (
            <ListSkeleton rows={5} />
          ) : (
            <div className="space-y-2">
              {list.map((exec) => {
                const isActive = exec.id === selectedId;
                return (
                  <button
                    key={exec.id}
                    onClick={() => router.push(`/executions?selected=${exec.id}`)}
                    className={`w-full text-left rounded-lg border p-3 transition-all ${
                      isActive
                        ? "border-[var(--color-accent)] bg-[var(--color-accent)]/5"
                        : "border-[var(--color-border)] bg-[var(--color-bg-secondary)] hover:border-[var(--color-text-secondary)]"
                    }`}
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-[var(--color-text-primary)] truncate">
                          {exec.goal}
                        </p>
                        <p className="text-xs text-[var(--color-text-secondary)] mt-1">
                          {new Date(exec.created_at).toLocaleDateString(undefined, {
                            month: "short",
                            day: "numeric",
                            hour: "2-digit",
                            minute: "2-digit",
                          })}
                        </p>
                      </div>
                      <ExecutionStatusBadge status={exec.status} />
                    </div>
                    {isActive && exec.progress > 0 && (
                      <div className="mt-2 h-1 rounded-full bg-[var(--color-bg-primary)]">
                        <div
                          className="h-1 rounded-full bg-[var(--color-accent)] transition-all"
                          style={{ width: `${Math.min(100, exec.progress)}%` }}
                        />
                      </div>
                    )}
                  </button>
                );
              })}
              {list.length === 0 && !isLoading && (
                <div className="text-center py-8">
                  <p className="text-sm text-[var(--color-text-secondary)]">
                    No executions yet. Start one above!
                  </p>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Right: execution detail */}
        {selectedExecution && (
          <div className="lg:col-span-3 space-y-4">
            <ExecutionTimeline
              execution={selectedExecution}
              onCancel={() => handleCancel(selectedExecution.id)}
              onRetry={handleRetry}
            />

            {/* Artifacts section */}
            {selectedExecution.artifacts && selectedExecution.artifacts.length > 0 && (
              <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-4">
                <h3 className="text-sm font-semibold text-[var(--color-text-primary)] mb-3">
                  Artifacts ({selectedExecution.artifacts.length})
                </h3>
                <div className="space-y-2">
                  {selectedExecution.artifacts.map((artifactId, idx) => (
                    <div
                      key={artifactId || idx}
                      className="flex items-center justify-between rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] px-3 py-2"
                    >
                      <span className="text-sm text-[var(--color-text-primary)]">
                        Artifact {idx + 1}
                      </span>
                      <span className="text-xs text-[var(--color-text-secondary)]">
                        {artifactId}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* New execution form modal */}
      {showNewForm && (
        <ExecutionForm
          capability={null}
          onClose={() => setShowNewForm(false)}
        />
      )}
    </div>
  );
}

export default function ExecutionsPage() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <ExecutionsPageContent />
    </Suspense>
  );
}

// Re-used from execution-history
function ExecutionStatusBadge({ status }: { status: string }) {
  const colorMap: Record<string, string> = {
    pending: "bg-[var(--color-text-secondary)]/20 text-[var(--color-text-secondary)]",
    planning: "bg-yellow-900/30 text-yellow-400",
    running: "bg-blue-900/30 text-blue-400",
    waiting_approval: "bg-orange-900/30 text-orange-400",
    paused: "bg-yellow-900/30 text-yellow-400",
    completed: "bg-green-900/30 text-green-400",
    failed: "bg-red-900/30 text-red-400",
    cancelled: "bg-gray-900/30 text-gray-400",
  };

  return (
    <span className={`shrink-0 rounded-full px-2 py-0.5 text-[10px] font-medium ${colorMap[status] || colorMap.pending}`}>
      {status.replace(/_/g, " ")}
    </span>
  );
}

