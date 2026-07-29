"use client";

import { useState, useEffect, useCallback } from "react";
import { listCapabilities, getCapability } from "@/services/capability";
import { ExecutionForm } from "@/components/execution/execution-form";
import { CardSkeleton } from "@/components/ui/loading-skeleton";
import { useToast } from "@/components/ui/toast";
import type { Capability, CapabilityListResponse } from "@/types/capability";

const DOMAIN_ICONS: Record<string, string> = {
  network: "🌐",
  code: "💻",
  research: "🔬",
  devops: "⚙️",
  trading: "📈",
  society: "👥",
  self_development: "🧠",
  organization: "🏢",
};

export function CapabilityBrowser() {
  const [capabilities, setCapabilities] = useState<Capability[]>([]);
  const [domains, setDomains] = useState<string[]>([]);
  const [selected, setSelected] = useState<Capability | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeDomain, setActiveDomain] = useState<string>("all");
  const [showExecuteForm, setShowExecuteForm] = useState(false);
  const { showError: showToastError } = useToast();

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    listCapabilities()
      .then((data: CapabilityListResponse) => {
        if (!cancelled) {
          setCapabilities(data.capabilities || []);
          setDomains(data.domains || []);
        }
      })
      .catch((err: unknown) => {
        if (!cancelled) {
          const msg = err instanceof Error ? err.message : "Failed to load capabilities";
          setError(msg);
          showToastError("Failed to load capabilities", msg);
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => { cancelled = true; };
  }, [showToastError]);

  const handleSelect = useCallback(async (capability: Capability) => {
    setError(null);
    setSelected(capability);
    try {
      const detail = await getCapability(capability.id);
      setSelected(detail);
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Failed to load capability detail";
      setError(msg);
      showToastError("Failed to load detail", msg);
    }
  }, [showToastError]);

  const filteredCapabilities = activeDomain === "all"
    ? capabilities
    : capabilities.filter((c) => c.domain === activeDomain);

  // Loading state
  if (loading) {
    return (
      <div className="mx-auto max-w-5xl p-6 space-y-6">
        <div className="h-8 w-48 bg-[var(--color-bg-tertiary)] rounded animate-pulse" />
        <div className="h-4 w-64 bg-[var(--color-bg-tertiary)] rounded animate-pulse" />
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {Array.from({ length: 6 }).map((_, i) => (
            <CardSkeleton key={i} />
          ))}
        </div>
      </div>
    );
  }

  // Error state (no data)
  if (error && capabilities.length === 0) {
    return (
      <div className="mx-auto max-w-5xl p-6">
        <div className="rounded-xl border border-[var(--color-danger)] bg-[var(--color-bg-secondary)] p-6 text-center">
          <p className="text-lg mb-2">⚠️</p>
          <p className="text-sm font-medium text-[var(--color-text-primary)]">Failed to load capabilities</p>
          <p className="text-xs text-[var(--color-text-secondary)] mt-1">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="mt-4 rounded-lg bg-[var(--color-accent)] px-4 py-2 text-sm text-white hover:opacity-90"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-5xl p-6 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-[var(--color-text-primary)]">
          Capability Explorer
        </h1>
        <p className="text-sm text-[var(--color-text-secondary)] mt-1">
          Browse available capabilities and execute tasks
        </p>
      </div>

      {/* Domain filter pills */}
      {domains.length > 0 && (
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setActiveDomain("all")}
            className={`rounded-full px-4 py-1.5 text-xs font-medium transition-colors ${
              activeDomain === "all"
                ? "bg-[var(--color-accent)] text-white"
                : "border border-[var(--color-border)] text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-tertiary)]"
            }`}
          >
            All ({capabilities.length})
          </button>
          {domains.map((domain) => {
            const count = capabilities.filter((c) => c.domain === domain).length;
            const icon = DOMAIN_ICONS[domain] || "📦";
            return (
              <button
                key={domain}
                onClick={() => setActiveDomain(domain)}
                className={`rounded-full px-4 py-1.5 text-xs font-medium transition-colors ${
                  activeDomain === domain
                    ? "bg-[var(--color-accent)] text-white"
                    : "border border-[var(--color-border)] text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-tertiary)]"
                }`}
              >
                {icon} {domain.replace(/_/g, " ")} ({count})
              </button>
            );
          })}
        </div>
      )}

      {/* Capability grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredCapabilities.map((cap) => {
          const isSelected = selected?.id === cap.id;
          return (
            <button
              key={cap.id}
              onClick={() => handleSelect(cap)}
              className={`rounded-xl border p-4 text-left transition-all ${
                isSelected
                  ? "border-[var(--color-accent)] bg-[var(--color-accent)]/5 shadow-sm"
                  : "border-[var(--color-border)] bg-[var(--color-bg-secondary)] hover:border-[var(--color-text-secondary)] hover:shadow-sm"
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="text-lg">{DOMAIN_ICONS[cap.domain] || "🧩"}</span>
                    <p className="text-sm font-semibold text-[var(--color-text-primary)] truncate">
                      {cap.name}
                    </p>
                  </div>
                  <p className="text-xs text-[var(--color-text-secondary)] mt-2 line-clamp-2">
                    {cap.description || "No description available"}
                  </p>
                </div>
              </div>

              {cap.tags && cap.tags.length > 0 && (
                <div className="mt-3 flex flex-wrap gap-1">
                  {cap.tags.slice(0, 3).map((tag) => (
                    <span
                      key={tag}
                      className="rounded-full bg-[var(--color-bg-primary)] px-2 py-0.5 text-[10px] text-[var(--color-text-secondary)]"
                    >
                      {tag}
                    </span>
                  ))}
                  {cap.tags.length > 3 && (
                    <span className="text-[10px] text-[var(--color-text-secondary)]">
                      +{cap.tags.length - 3}
                    </span>
                  )}
                </div>
              )}

              {cap.skills && cap.skills.length > 0 && (
                <div className="mt-2 flex flex-wrap gap-1">
                  {cap.skills.slice(0, 2).map((skill) => (
                    <span
                      key={skill}
                      className="rounded bg-[var(--color-accent)]/10 px-1.5 py-0.5 text-[10px] text-[var(--color-accent)]"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              )}
            </button>
          );
        })}
      </div>

      {filteredCapabilities.length === 0 && (
        <div className="text-center py-12">
          <p className="text-lg mb-2">🔍</p>
          <p className="text-sm text-[var(--color-text-secondary)]">
            No capabilities found for this domain.
          </p>
        </div>
      )}

      {/* Detail panel when capability selected */}
      {selected && (
        <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-6 space-y-6">
          {/* Detail header */}
          <div className="flex items-start justify-between">
            <div>
              <div className="flex items-center gap-2">
                <span className="text-2xl">{DOMAIN_ICONS[selected.domain] || "🧩"}</span>
                <div>
                  <h2 className="text-lg font-semibold text-[var(--color-text-primary)]">
                    {selected.name}
                  </h2>
                  <p className="text-xs text-[var(--color-text-secondary)]">
                    {selected.domain.replace(/_/g, " ")} · v{selected.complexity || "1.0"}
                  </p>
                </div>
              </div>
              <p className="text-sm text-[var(--color-text-secondary)] mt-3">
                {selected.description || "No description available."}
              </p>
            </div>
            <button
              onClick={() => setShowExecuteForm(true)}
              className="rounded-lg bg-[var(--color-accent)] px-5 py-2.5 text-sm font-medium text-white hover:opacity-90 transition-opacity flex items-center gap-2"
            >
              🚀 Execute
            </button>
          </div>

          {/* Skills / Tags / Workers */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <p className="text-xs font-semibold uppercase tracking-wide text-[var(--color-text-secondary)] mb-2">Skills</p>
              {selected.skills && selected.skills.length > 0 ? (
                <div className="flex flex-wrap gap-1.5">
                  {selected.skills.map((skill) => (
                    <span key={skill} className="rounded-lg bg-[var(--color-bg-primary)] px-2.5 py-1 text-xs text-[var(--color-text-secondary)]">
                      {skill}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="text-xs text-[var(--color-text-secondary)]">None specified</p>
              )}
            </div>
            <div>
              <p className="text-xs font-semibold uppercase tracking-wide text-[var(--color-text-secondary)] mb-2">Tags</p>
              {selected.tags && selected.tags.length > 0 ? (
                <div className="flex flex-wrap gap-1.5">
                  {selected.tags.map((tag) => (
                    <span key={tag} className="rounded-full bg-[var(--color-bg-primary)] px-2.5 py-1 text-xs text-[var(--color-text-secondary)]">
                      {tag}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="text-xs text-[var(--color-text-secondary)]">None specified</p>
              )}
            </div>
            <div>
              <p className="text-xs font-semibold uppercase tracking-wide text-[var(--color-text-secondary)] mb-2">Workers</p>
              {selected.workers && selected.workers.length > 0 ? (
                <div className="flex flex-wrap gap-1.5">
                  {selected.workers.map((worker) => (
                    <span key={worker} className="rounded-full bg-[var(--color-accent)]/10 px-2.5 py-1 text-xs text-[var(--color-accent)]">
                      {worker}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="text-xs text-[var(--color-text-secondary)]">Auto-assigned</p>
              )}
            </div>
          </div>

          {/* Subtask templates */}
          {selected.subtask_templates && selected.subtask_templates.length > 0 && (
            <div>
              <p className="text-xs font-semibold uppercase tracking-wide text-[var(--color-text-secondary)] mb-3">
                Task Templates ({selected.subtask_templates.length})
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                {selected.subtask_templates.map((task) => (
                  <div key={task.id} className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] p-3">
                    <p className="text-sm font-medium text-[var(--color-text-primary)]">{task.name}</p>
                    {task.description && (
                      <p className="text-xs text-[var(--color-text-secondary)] mt-1">{task.description}</p>
                    )}
                    {task.required_skills && task.required_skills.length > 0 && (
                      <div className="mt-2 flex flex-wrap gap-1">
                        {task.required_skills.map((skill) => (
                          <span key={skill} className="rounded bg-[var(--color-accent)]/10 px-1.5 py-0.5 text-[10px] text-[var(--color-accent)]">
                            {skill}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Dependencies */}
          {selected.dependencies && selected.dependencies.length > 0 && (
            <div>
              <p className="text-xs font-semibold uppercase tracking-wide text-[var(--color-text-secondary)] mb-2">Dependencies</p>
              <div className="flex flex-wrap gap-1.5">
                {selected.dependencies.map((dep) => (
                  <span key={dep} className="rounded-lg border border-[var(--color-border)] px-2.5 py-1 text-xs text-[var(--color-text-secondary)]">
                    {dep}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Related capabilities */}
          {selected.related_capabilities && selected.related_capabilities.length > 0 && (
            <div>
              <p className="text-xs font-semibold uppercase tracking-wide text-[var(--color-text-secondary)] mb-2">Related Capabilities</p>
              <div className="flex flex-wrap gap-1.5">
                {selected.related_capabilities.map((rel) => (
                  <button
                    key={rel}
                    onClick={() => {
                      const found = capabilities.find((c) => c.id === rel || c.name === rel);
                      if (found) handleSelect(found);
                    }}
                    className="rounded-lg border border-[var(--color-border)] px-2.5 py-1 text-xs text-[var(--color-accent)] hover:bg-[var(--color-accent)]/10 transition-colors"
                  >
                    {rel}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Execution form modal */}
      {showExecuteForm && selected && (
        <ExecutionForm
          capability={selected}
          onClose={() => setShowExecuteForm(false)}
        />
      )}
    </div>
  );
}

