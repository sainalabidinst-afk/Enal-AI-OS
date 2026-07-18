"use client";

import { useState } from "react";
import { useExecutionStore } from "@/store/execution-store";
import { useWorkspaceStore } from "@/store/workspace-store";
import { ExecutionHistoryPanel } from "@/components/execution/execution-history";

export default function ExecutionsPage() {
  const [goal, setGoal] = useState("");
  const startExecution = useExecutionStore((s) => s.startExecution);
  const retryExecution = useExecutionStore((s) => s.retryExecution);
  const workspace = useWorkspaceStore();

  const handleStart = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!goal.trim()) return;
    const wsId = workspace.activeWorkspaceId || workspace.workspaces[0]?.id;
    if (!wsId) {
      alert("Please create or select a workspace first.");
      return;
    }
    await startExecution(goal.trim(), wsId);
    setGoal("");
  };

  const handleRetry = async (executionGoal: string) => {
    const wsId = workspace.activeWorkspaceId || workspace.workspaces[0]?.id;
    if (!wsId) {
      alert("Please create or select a workspace first.");
      return;
    }
    await retryExecution(executionGoal, wsId);
  };

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-6">
      <h1 className="text-xl font-bold">Executions</h1>

      <form onSubmit={handleStart} className="flex gap-2">
        <input
          value={goal}
          onChange={(e) => setGoal(e.target.value)}
          placeholder="Enter a goal to execute..."
          className="flex-1 rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] px-4 py-2 text-sm focus:border-[var(--color-accent)] focus:outline-none"
        />
        <button
          type="submit"
          disabled={!goal.trim()}
          className="rounded-lg bg-[var(--color-accent)] px-4 py-2 text-sm text-white hover:opacity-90 disabled:opacity-50"
        >
          Run
        </button>
      </form>

      <ExecutionHistoryPanel
        selectedExecutionId={null}
        onSelectExecution={() => {}}
        onRetry={handleRetry}
      />
    </div>
  );
}
