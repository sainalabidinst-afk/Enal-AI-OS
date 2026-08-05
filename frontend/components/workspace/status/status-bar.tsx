"use client";

import { useWorkspaceStore } from "@/components/workspace/stores/workspace-store";

export function StatusBar() {
  const activeApp = useWorkspaceStore((s) => s.activeApp);
  const panel = useWorkspaceStore((s) => s.panel);

  return (
    <footer className="flex h-6 shrink-0 items-center justify-between border-t border-[var(--color-border)] bg-[var(--color-surface)] px-3 text-[10px] text-[var(--color-secondary-500)]" aria-label="Status bar">
      <div className="flex items-center gap-3">
        <span>ENAL AI OS</span>
        <span>Workspace: {activeApp}</span>
        {panel.right.open && <span>Right Panel</span>}
        {panel.bottom.open && <span>Bottom Panel</span>}
      </div>
      <div className="flex items-center gap-3">
        <span>Ready</span>
        <span>UTF-8</span>
        <span aria-live="polite">{new Date().toLocaleTimeString()}</span>
      </div>
    </footer>
  );
}
