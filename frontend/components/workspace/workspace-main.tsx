"use client";

import { ReactNode } from "react";
import { useWorkspaceEngineStore } from "@/store/workspace-engine-store";

export function WorkspaceMain({ children, app }: { children: ReactNode; app: string }) {
  return (
    <main className="flex-1 overflow-y-auto bg-[var(--color-bg-primary)]">
      {children}
    </main>
  );
}
