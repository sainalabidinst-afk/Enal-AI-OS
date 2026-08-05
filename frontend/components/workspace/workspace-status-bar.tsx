"use client";

import { useWorkspaceEngineStore } from "@/store/workspace-engine-store";

export function WorkspaceStatusBar() {
  const activeApp = useWorkspaceEngineStore((s) => s.activeApp);
  const panel = useWorkspaceEngineStore((s) => s.panel);

  return (
    <footer className="flex h-6 shrink-0 items-center justify-between border-t border-[var(--color-border)] bg-[var(--color-bg-secondary)] px-3 text-[10px] text-[var(--color-text-secondary)]">
      <div className="flex items-center gap-3">
        <span>ENAL AI OS</span>
        <span>Workspace: {activeApp}</span>
        {panel.right.open && <span>Right Panel</span>}
        {panel.bottom.open && <span>Bottom Panel</span>}
      </div>
      <div className="flex items-center gap-3">
        <span>Ready</span>
        <span>UTF-8</span>
        <span>{new Date().toLocaleTimeString()}</span>
      </div>
    </footer>
  );
}
