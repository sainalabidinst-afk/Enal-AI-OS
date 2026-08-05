"use client";

import { useEffect } from "react";
import { usePathname } from "next/navigation";
import { useWorkspaceEngineStore } from "@/store/workspace-engine-store";

const APP_MAP: Record<string, "trading" | "network" | "code" | "security" | "research"> = {
  trading: "trading",
  network: "network",
  code: "code",
  security: "security",
  research: "research",
};

export function WorkspaceProvider({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const setActiveApp = useWorkspaceEngineStore((s) => s.setActiveApp);

  useEffect(() => {
    const segments = pathname.split("/").filter(Boolean);
    const appSegment = segments[1];
    if (appSegment && APP_MAP[appSegment]) {
      setActiveApp(APP_MAP[appSegment]);
    }
  }, [pathname, setActiveApp]);

  return <>{children}</>;
}
