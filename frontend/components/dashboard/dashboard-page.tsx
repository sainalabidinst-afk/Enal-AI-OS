"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/store/auth-store";
import { useWorkspaceStore } from "@/store/workspace-store";
import { useExecutionStore } from "@/store/execution-store";
import { listCapabilities } from "@/services/capability";
import { useToast } from "@/components/ui/toast";
import { StatsCards } from "./stats-cards";
import { RecentExecutions } from "./recent-executions";
import { PageSkeleton } from "@/components/ui/loading-skeleton";
import type { CapabilityListResponse } from "@/types/capability";

export function DashboardPage() {
  const router = useRouter();
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const { showError } = useToast();

  const workspaces = useWorkspaceStore((s) => s.workspaces);
  const loadWorkspaces = useWorkspaceStore((s) => s.loadWorkspaces);
  const executions = useExecutionStore((s) => s.executions);
  const loadExecutions = useExecutionStore((s) => s.loadExecutions);

  const [capabilityCount, setCapabilityCount] = useState(0);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/login");
      return;
    }

    let cancelled = false;

    async function load() {
      try {
        const [caps] = await Promise.all([
          listCapabilities(),
          loadWorkspaces(),
          loadExecutions(),
        ]);

        if (!cancelled) {
          setCapabilityCount(caps.capabilities?.length || 0);
        }
      } catch (error) {
        if (!cancelled) {
          showError("Failed to load dashboard data", error instanceof Error ? error.message : undefined);
        }
      } finally {
        if (!cancelled) {
          setIsLoading(false);
        }
      }
    }

    load();
    return () => { cancelled = true; };
  }, [isAuthenticated, router, loadWorkspaces, loadExecutions, showError]);

  if (isLoading) {
    return <PageSkeleton />;
  }

  const executionList = Object.values(executions);
  const activeCount = executionList.filter(
    (e) => ["pending", "planning", "running", "waiting_approval"].includes(e.status)
  ).length;
  const completedCount = executionList.filter(
    (e) => e.status === "completed"
  ).length;

  const handleSelectExecution = (id: string) => {
    router.push(`/executions?selected=${id}`);
  };

  return (
    <div className="mx-auto max-w-5xl p-6 space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-[var(--color-text-primary)]">
          Dashboard
        </h1>
        <p className="text-sm text-[var(--color-text-secondary)] mt-1">
          Platform overview and recent activity
        </p>
      </div>

      {/* Stats */}
      <StatsCards
        capabilities={capabilityCount}
        workspaces={workspaces.length}
        activeExecutions={activeCount}
        completedExecutions={completedCount}
        isLoading={isLoading}
      />

      {/* Quick actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <a
          href="/executions"
          className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-4 hover:border-[var(--color-accent)] transition-colors group"
        >
          <p className="text-sm font-medium text-[var(--color-text-primary)] group-hover:text-[var(--color-accent)]">
            🚀 New Execution
          </p>
          <p className="text-xs text-[var(--color-text-secondary)] mt-1">
            Start a new capability execution
          </p>
        </a>
        <a
          href="/workspace"
          className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-4 hover:border-[var(--color-accent)] transition-colors group"
        >
          <p className="text-sm font-medium text-[var(--color-text-primary)] group-hover:text-[var(--color-accent)]">
            📁 Manage Workspaces
          </p>
          <p className="text-xs text-[var(--color-text-secondary)] mt-1">
            Browse and manage workspace files
          </p>
        </a>
        <a
          href="/capabilities"
          className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-4 hover:border-[var(--color-accent)] transition-colors group"
        >
          <p className="text-sm font-medium text-[var(--color-text-primary)] group-hover:text-[var(--color-accent)]">
            🧩 Explore Capabilities
          </p>
          <p className="text-xs text-[var(--color-text-secondary)] mt-1">
            View available capability packs
          </p>
        </a>
      </div>

      {/* Recent executions */}
      <RecentExecutions
        executions={executionList}
        isLoading={isLoading}
        onSelect={handleSelectExecution}
      />
    </div>
  );
}

