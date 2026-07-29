"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useExecutionStore } from "@/store/execution-store";
import { useWorkspaceStore } from "@/store/workspace-store";
import { useToast } from "@/components/ui/toast";
import type { Capability } from "@/types/capability";

interface ExecutionFormProps {
  capability?: Capability | null;
  onClose: () => void;
}

export function ExecutionForm({ capability, onClose }: ExecutionFormProps) {
  const router = useRouter();
  const [goal, setGoal] = useState(capability ? `Run ${capability.name}: ` : "");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const startExecution = useExecutionStore((s) => s.startExecution);
  const workspaces = useWorkspaceStore((s) => s.workspaces);
  const loadWorkspaces = useWorkspaceStore((s) => s.loadWorkspaces);
  const [selectedWorkspaceId, setSelectedWorkspaceId] = useState<string>("");
  const { showSuccess, showError } = useToast();

  // Load workspaces on mount
  useState(() => {
    if (workspaces.length === 0) {
      loadWorkspaces().catch(() => {});
    }
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!goal.trim()) {
      showError("Validation Error", "Please enter a goal.");
      return;
    }

    const wsId = selectedWorkspaceId || workspaces[0]?.id;
    if (!wsId) {
      showError("Workspace Required", "Please create or select a workspace first.");
      return;
    }

    setIsSubmitting(true);
    try {
      const execution = await startExecution(goal.trim(), wsId);
      if (execution) {
        showSuccess("Execution Started", `Goal: ${goal.trim().slice(0, 60)}...`);
        onClose();
        router.push(`/executions?selected=${execution.id}`);
      } else {
        showError("Failed to start execution");
      }
    } catch (err) {
      showError(
        "Execution Error",
        err instanceof Error ? err.message : "An unexpected error occurred"
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <div
        className="w-full max-w-lg rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between border-b border-[var(--color-border)] px-6 py-4">
          <h2 className="text-lg font-semibold text-[var(--color-text-primary)]">
            New Execution
          </h2>
          <button
            onClick={onClose}
            className="text-sm text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)] transition-colors"
          >
            ✕
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {capability && (
            <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] p-3">
              <p className="text-xs font-medium text-[var(--color-text-secondary)] uppercase tracking-wide">
                Capability
              </p>
              <p className="text-sm font-medium text-[var(--color-text-primary)] mt-1">
                {capability.name}
              </p>
              {capability.description && (
                <p className="text-xs text-[var(--color-text-secondary)] mt-0.5">
                  {capability.description}
                </p>
              )}
            </div>
          )}

          {/* Goal */}
          <div className="space-y-2">
            <label
              htmlFor="goal"
              className="block text-sm font-medium text-[var(--color-text-primary)]"
            >
              Goal / Task Description
            </label>
            <textarea
              id="goal"
              value={goal}
              onChange={(e) => setGoal(e.target.value)}
              placeholder="Describe what you want to accomplish..."
              rows={4}
              className="w-full rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] px-4 py-2.5 text-sm text-[var(--color-text-primary)] placeholder:text-[var(--color-text-secondary)] focus:border-[var(--color-accent)] focus:outline-none focus:ring-1 focus:ring-[var(--color-accent)] resize-none"
            />
          </div>

          {/* Workspace selector */}
          <div className="space-y-2">
            <label
              htmlFor="workspace"
              className="block text-sm font-medium text-[var(--color-text-primary)]"
            >
              Workspace
            </label>
            <select
              id="workspace"
              value={selectedWorkspaceId}
              onChange={(e) => setSelectedWorkspaceId(e.target.value)}
              className="w-full rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] px-4 py-2.5 text-sm text-[var(--color-text-primary)] focus:border-[var(--color-accent)] focus:outline-none focus:ring-1 focus:ring-[var(--color-accent)]"
            >
              {workspaces.length === 0 && (
                <option value="">No workspaces available</option>
              )}
              {workspaces.map((ws) => (
                <option key={ws.id} value={ws.id}>
                  {ws.name || ws.id}
                </option>
              ))}
            </select>
          </div>

          {/* Actions */}
          <div className="flex items-center justify-end gap-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="rounded-lg border border-[var(--color-border)] px-4 py-2 text-sm text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-tertiary)] transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting || !goal.trim()}
              className="rounded-lg bg-[var(--color-accent)] px-6 py-2 text-sm font-medium text-white hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed transition-opacity"
            >
              {isSubmitting ? (
                <span className="flex items-center gap-2">
                  <span className="inline-block h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white" />
                  Starting...
                </span>
              ) : (
                "Start Execution"
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

