"use client";

import { useEffect, useState } from "react";
import { useArtifactStore } from "@/store/artifact-store";
import { useWorkspaceStore } from "@/store/workspace-store";
import { ArtifactCard } from "@/components/artifact/artifact-card";
import { CardSkeleton, ListSkeleton } from "@/components/ui/loading-skeleton";
import { useToast } from "@/components/ui/toast";
import { ErrorBoundary } from "@/components/ui/error-boundary";

function ArtifactsPageContent() {
  const [loading, setLoading] = useState(true);
  const [filterType, setFilterType] = useState<string>("all");

  const artifacts = useArtifactStore((s) => s.artifacts);
  const loadArtifacts = useArtifactStore((s) => s.loadArtifacts);
  const activeWorkspaceId = useWorkspaceStore((s) => s.activeWorkspaceId);
  const workspaces = useWorkspaceStore((s) => s.workspaces);
  const loadWorkspaces = useWorkspaceStore((s) => s.loadWorkspaces);
  const { showError } = useToast();

  // Load artifacts on mount
  useEffect(() => {
    let cancelled = false;
    setLoading(true);

    async function load() {
      try {
        // Load workspaces if needed
        if (workspaces.length === 0) {
          await loadWorkspaces();
        }
        // Load artifacts for active workspace, or all
        await loadArtifacts(activeWorkspaceId || undefined);
      } catch (err) {
        if (!cancelled) {
          showError("Failed to load artifacts", err instanceof Error ? err.message : undefined);
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    load();
    return () => { cancelled = true; };
  }, [activeWorkspaceId, loadArtifacts, loadWorkspaces, workspaces.length, showError]);

  // Derive unique artifact types for filter
  const artifactTypes = Array.from(new Set(artifacts.map((a) => a.type)));
  const filtered = filterType === "all"
    ? artifacts
    : artifacts.filter((a) => a.type === filterType);

  // Loading state
  if (loading) {
    return (
      <div className="mx-auto max-w-5xl p-6 space-y-6">
        <div className="h-8 w-48 bg-[var(--color-bg-tertiary)] rounded animate-pulse" />
        <div className="h-4 w-64 bg-[var(--color-bg-tertiary)] rounded animate-pulse" />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {Array.from({ length: 4 }).map((_, i) => (
            <CardSkeleton key={i} />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-5xl p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-[var(--color-text-primary)]">
            Artifacts
          </h1>
          <p className="text-sm text-[var(--color-text-secondary)] mt-1">
            Browse and manage execution artifacts
            {activeWorkspaceId && (
              <span> — Workspace: {workspaces.find((w) => w.id === activeWorkspaceId)?.name || activeWorkspaceId}</span>
            )}
          </p>
        </div>
        <button
          onClick={() => loadArtifacts(activeWorkspaceId || undefined)}
          className="rounded-lg border border-[var(--color-border)] px-3 py-1.5 text-xs text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-tertiary)] transition-colors"
        >
          Refresh
        </button>
      </div>

      {/* Type filter */}
      {artifactTypes.length > 1 && (
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setFilterType("all")}
            className={`rounded-full px-4 py-1.5 text-xs font-medium transition-colors ${
              filterType === "all"
                ? "bg-[var(--color-accent)] text-white"
                : "border border-[var(--color-border)] text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-tertiary)]"
            }`}
          >
            All ({artifacts.length})
          </button>
          {artifactTypes.map((type) => {
            const count = artifacts.filter((a) => a.type === type).length;
            return (
              <button
                key={type}
                onClick={() => setFilterType(type)}
                className={`rounded-full px-4 py-1.5 text-xs font-medium transition-colors ${
                  filterType === type
                    ? "bg-[var(--color-accent)] text-white"
                    : "border border-[var(--color-border)] text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-tertiary)]"
                }`}
              >
                {type.replace(/_/g, " ")} ({count})
              </button>
            );
          })}
        </div>
      )}

      {/* Artifact grid */}
      {filtered.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-lg mb-2">📄</p>
          <p className="text-sm text-[var(--color-text-secondary)]">
            {artifacts.length === 0
              ? "No artifacts yet. Artifacts are created when capabilities execute and produce results."
              : "No artifacts match the selected filter."}
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filtered.map((artifact) => (
            <ArtifactCard key={artifact.id} artifact={artifact} />
          ))}
        </div>
      )}

      {/* Summary */}
      {artifacts.length > 0 && (
        <p className="text-xs text-[var(--color-text-secondary)] text-center">
          Showing {filtered.length} of {artifacts.length} artifact{artifacts.length !== 1 ? "s" : ""}
        </p>
      )}
    </div>
  );
}

export default function ArtifactsPage() {
  return (
    <ErrorBoundary>
      <ArtifactsPageContent />
    </ErrorBoundary>
  );
}

