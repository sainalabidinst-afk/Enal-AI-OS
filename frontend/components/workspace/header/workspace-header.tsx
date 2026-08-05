"use client";

import { useRouter } from "next/navigation";
import { useAuthStore } from "@/store/auth-store";
import { useWorkspaceStore } from "@/components/workspace/stores/workspace-store";
import { Button } from "@/components/design-system/primitives/button";
import { Avatar } from "@/components/design-system/primitives/avatar";
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

  const handleLogout = async () => {
    await logout();
    router.push("/login");
  };

  return (
    <header className="flex h-12 shrink-0 items-center justify-between border-b border-[var(--color-border)] bg-[var(--color-surface)] px-4">
      <div className="flex items-center gap-4">
        <button
          onClick={() => router.push("/dashboard")}
          className="flex items-center gap-2 hover:opacity-80 transition-opacity"
          aria-label="Go to dashboard"
        >
          <span className="text-lg">🧠</span>
          <span className="text-sm font-semibold">Enal AI OS</span>
        </button>
        <Breadcrumb />
      </div>

      <div className="flex items-center gap-2">
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
        <span className="text-xs text-[var(--color-secondary-500)]">{user?.username || "User"}</span>
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
