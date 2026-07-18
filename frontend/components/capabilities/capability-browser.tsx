"use client";

import { useState, useEffect } from "react";
import { listCapabilities, getCapability } from "@/services/capability";
import type { Capability, CapabilityListResponse } from "@/types/capability";

export function CapabilityBrowser() {
  const [capabilities, setCapabilities] = useState<Capability[]>([]);
  const [domains, setDomains] = useState<string[]>([]);
  const [selected, setSelected] = useState<Capability | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [running, setRunning] = useState(false);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    listCapabilities()
      .then((data: CapabilityListResponse) => {
        if (!cancelled) {
          setCapabilities(data.capabilities || []);
          setDomains(data.domains || []);
        }
      })
      .catch((err) => {
        if (!cancelled) setError(err instanceof Error ? err.message : "Failed to load capabilities");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => { cancelled = true; };
  }, []);

  const handleSelect = async (capability: Capability) => {
    setError(null);
    try {
      const detail = await getCapability(capability.id);
      setSelected(detail);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load capability detail");
    }
  };

  const handleRun = async () => {
    if (!selected) return;
    setRunning(true);
    try {
      const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const response = await fetch(`${base}/api/v1/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: `Run ${selected.name} capability`,
          stream: false,
        }),
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      alert(`Execution started: ${data.conversation_id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to run capability");
    } finally {
      setRunning(false);
    }
  };

  if (loading) return <p className="text-sm text-[var(--color-text-secondary)]">Loading capabilities...</p>;
  if (error) return <div className="rounded-lg border border-[var(--color-danger)] bg-[var(--color-bg-secondary)] px-4 py-2 text-sm text-[var(--color-danger)]">{error}</div>;

  return (
    <div className="max-w-5xl mx-auto p-6 space-y-6">
      <div>
        <h1 className="text-xl font-bold">Capabilities</h1>
        <p className="text-sm text-[var(--color-text-secondary)]">Browse and run available capabilities</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {capabilities.map((cap) => (
          <button
            key={cap.id}
            onClick={() => handleSelect(cap)}
            className={`rounded-lg border p-4 text-left transition-colors ${
              selected?.id === cap.id
                ? "border-[var(--color-accent)] bg-[var(--color-bg-secondary)]"
                : "border-[var(--color-border)] bg-[var(--color-bg-secondary)] hover:border-[var(--color-text-secondary)]"
            }`}
          >
            <p className="text-sm font-medium">{cap.name}</p>
            <p className="text-xs text-[var(--color-text-secondary)] mt-1 line-clamp-2">{cap.description}</p>
            <div className="mt-2 flex flex-wrap gap-1">
              {cap.tags?.slice(0, 3).map((tag) => (
                <span key={tag} className="rounded-full bg-[var(--color-bg-primary)] px-2 py-0.5 text-xs text-[var(--color-text-secondary)]">
                  {tag}
                </span>
              ))}
            </div>
          </button>
        ))}
      </div>

      {selected && (
        <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-6 space-y-4">
          <div className="flex items-start justify-between">
            <div>
              <h2 className="text-lg font-semibold">{selected.name}</h2>
              <p className="text-sm text-[var(--color-text-secondary)] mt-1">{selected.description}</p>
            </div>
            <button
              onClick={handleRun}
              disabled={running}
              className="rounded-lg bg-[var(--color-accent)] px-4 py-2 text-sm text-white hover:opacity-90 disabled:opacity-50"
            >
              {running ? "Running..." : "Run Capability"}
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p className="text-xs font-semibold uppercase tracking-wide text-[var(--color-text-secondary)]">Skills</p>
              <div className="mt-2 flex flex-wrap gap-1">
                {selected.skills?.map((skill) => (
                  <span key={skill} className="rounded-full bg-[var(--color-bg-primary)] px-2 py-0.5 text-xs text-[var(--color-text-secondary)]">
                    {skill}
                  </span>
                ))}
              </div>
            </div>
            <div>
              <p className="text-xs font-semibold uppercase tracking-wide text-[var(--color-text-secondary)]">Tags</p>
              <div className="mt-2 flex flex-wrap gap-1">
                {selected.tags?.map((tag) => (
                  <span key={tag} className="rounded-full bg-[var(--color-bg-primary)] px-2 py-0.5 text-xs text-[var(--color-text-secondary)]">
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          </div>

          {selected.subtask_templates && selected.subtask_templates.length > 0 && (
            <div>
              <p className="text-xs font-semibold uppercase tracking-wide text-[var(--color-text-secondary)]">Task Templates</p>
              <div className="mt-2 space-y-2">
                {selected.subtask_templates.map((task) => (
                  <div key={task.id} className="rounded-md border border-[var(--color-border)] bg-[var(--color-bg-primary)] p-3">
                    <p className="text-sm font-medium">{task.name}</p>
                    <p className="text-xs text-[var(--color-text-secondary)] mt-1">{task.description}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
