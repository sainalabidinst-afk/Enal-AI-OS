"use client";

import { useEffect } from "react";
import { useSettingsStore } from "@/store/settings-store";
import { useWorkspaceStore } from "@/store/workspace-store";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export function Providers({ children }: { children: React.ReactNode }) {
  const theme = useSettingsStore((s) => s.theme);
  const loadWorkspaces = useWorkspaceStore((s) => s.loadWorkspaces);

  useEffect(() => {
    const root = document.documentElement;
    if (theme === "system") {
      const media = window.matchMedia("(prefers-color-scheme: dark)");
      root.dataset.theme = media.matches ? "dark" : "light";
      const handler = (e: MediaQueryListEvent) => {
        root.dataset.theme = e.matches ? "dark" : "light";
      };
      media.addEventListener("change", handler);
      return () => media.removeEventListener("change", handler);
    }
    root.dataset.theme = theme;
  }, [theme]);

  useEffect(() => {
    const token = localStorage.getItem("enal-auth-token");
    if (token) {
      loadWorkspaces().catch(() => {});
    }
  }, [loadWorkspaces]);

  return <>{children}</>;
}
