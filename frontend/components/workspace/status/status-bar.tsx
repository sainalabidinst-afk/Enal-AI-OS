"use client";

import { useWorkspaceStore } from "@/components/workspace/stores/workspace-store";
import { cn } from "@/lib/utils";

export function StatusBar() {
  const activeApp = useWorkspaceStore((s) => s.activeApp);
  const panel = useWorkspaceStore((s) => s.panel);
  const system = useWorkspaceStore((s) => s.system);
  const activeWorkspace = useWorkspaceStore((s) => s.workspaces.find((w) => w.active)?.name || "");

  const latencyClass =
    system.latencyMs > 300
      ? "text-[var(--color-danger)]"
      : system.latencyMs > 100
        ? "text-[var(--color-warning)]"
        : "text-[var(--color-success)]";

  return (
    <footer
      className="flex h-6 shrink-0 items-center justify-between border-t border-[var(--color-border)] bg-[var(--color-surface)] px-3 text-[10px]"
      aria-label="Status bar"
    >
      <div className="flex items-center gap-3 text-[var(--color-text-secondary)]">
        <span className="text-[var(--color-text-secondary)]">ENAL AI OS</span>
        <span>Workspace: {activeWorkspace || activeApp}</span>
        {panel.right.open && <span>Right Panel</span>}
        {panel.bottom.open && <span>Bottom Panel</span>}
      </div>

      <div className="flex items-center gap-3 text-[var(--color-text-secondary)]">
        <span className={cn("font-medium", latencyClass)}>
          Latency: {system.latencyMs}ms
        </span>
        <span className={cn("inline-block h-2 w-2 rounded-full", system.online ? "bg-[var(--color-success)]" : "bg-[var(--color-danger)]")} />
        <span>{new Date().toLocaleTimeString()}</span>
      </div>
    </footer>
  );
}
