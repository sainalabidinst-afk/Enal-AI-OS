"use client";

import { type ReactNode, useEffect } from "react";
import { usePathname, useRouter } from "next/navigation";
import { useWorkspaceStore } from "@/components/workspace/stores/workspace-store";
import { WorkspaceContext } from "@/components/workspace/engine/workspace-context";

const APP_MAP: Record<string, import("@/components/workspace/stores/workspace-store").WorkspaceApp> = {
  trading: "trading",
  network: "network",
  code: "code",
  security: "security",
  research: "research",
  database: "database",
};

export function WorkspaceProvider({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const activeApp = useWorkspaceStore((s) => s.activeApp);
  const setActiveApp = useWorkspaceStore((s) => s.setActiveApp);

  useEffect(() => {
    const match = Object.entries(APP_MAP).find(([segment]) => pathname.includes(`/workspace/${segment}`));
    if (match) {
      const app = match[1];
      if (app !== activeApp) {
        setActiveApp(app);
      }
    }
  }, [pathname, activeApp, setActiveApp]);

  const store = useWorkspaceStore;

  return <WorkspaceContext.Provider value={store()}>{children}</WorkspaceContext.Provider>;
}
