"use client";

import { useRouter } from "next/navigation";
import { useAuthStore } from "@/store/auth-store";
import { useWorkspaceStore } from "@/components/workspace/stores/workspace-store";
import { Button } from "@/components/ui/button";
import { Avatar } from "@/components/ui/avatar";
import { Breadcrumb } from "@/components/workspace/header/breadcrumb";
import { WorkspaceSearch } from "@/components/workspace/header/workspace-search";
import { WorkspaceActions } from "@/components/workspace/header/workspace-actions";

export function WorkspaceHeader({
  onToggleRight,
  onToggleBottom,
}: {
  onToggleRight: () => void;
  onToggleBottom: () => void;
}) {
  const router = useRouter();
  const user = useAuthStore((s) => s.user);
  const logout = useAuthStore((s) => s.logout);
  const activeApp = useWorkspaceStore((s) => s.activeApp);
  const panel = useWorkspaceStore((s) => s.panel);
  const system = useWorkspaceStore((s) => s.system);

  const handleLogout = async () => {
    await logout();
    router.push("/login");
  };

  return (
    <header className="flex h-12 shrink-0 items-center justify-between gap-3 border-b border-[var(--color-border)] bg-[var(--color-surface)] px-4">
      <div className="flex items-center gap-4">
        <button
          onClick={() => router.push("/dashboard")}
          className="flex items-center gap-2 hover:opacity-80 transition-opacity"
          aria-label="Go to dashboard"
        >
          <span className="text-lg">🧠</span>
          <span className="text-sm font-semibold">Enal AI OS</span>
        </button>

        <div className="flex items-center gap-2 text-xs text-[var(--color-text-secondary)]">
          <span
            className={`inline-block h-2 w-2 rounded-full ${
              system.online
                ? "bg-[var(--color-success)] animate-pulse"
                : "bg-[var(--color-danger)]"
            }`}
          />
          <span>{system.online ? "Online" : "Offline"}</span>
          <span>•</span>
          <span>Model: {system.model}</span>
          {system.latencyMs > 0 && (
            <>
              <span>•</span>
              <span>{system.latencyMs}ms</span>
            </>
          )}
        </div>

        <Breadcrumb />
      </div>

      <div className="flex items-center gap-3">
        <WorkspaceSearch />
        <Button
          variant="ghost"
          size="icon"
          onClick={onToggleRight}
          aria-label={panel.right.open ? "Close right panel" : "Open right panel"}
          title={panel.right.open ? "Close right panel" : "Open right panel"}
        >
          {panel.right.open ? "◧" : "◨"}
        </Button>
        <Button
          variant="ghost"
          size="icon"
          onClick={onToggleBottom}
          aria-label={panel.bottom.open ? "Close bottom panel" : "Open bottom panel"}
          title={panel.bottom.open ? "Close bottom panel" : "Open bottom panel"}
        >
          {panel.bottom.open ? "⊟" : "⊞"}
        </Button>
        <WorkspaceActions />
        <Avatar fallback={user?.username || "U"} size="sm" />
        <span className="text-xs text-[var(--color-secondary-500)]">
          {user?.username || "User"}
        </span>
        <Button
          variant="ghost"
          size="sm"
          onClick={handleLogout}
          className="text-[var(--color-secondary-500)] hover:text-[var(--color-danger-500)]"
        >
          Sign out
        </Button>
      </div>
    </header>
  );
}
