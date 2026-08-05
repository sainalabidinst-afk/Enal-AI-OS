"use client";

import { usePathname, useRouter } from "next/navigation";
import {
  LayoutDashboard,
  LineChart,
  Network,
  Code2,
  Shield,
  FlaskConical,
  PanelRightClose,
  PanelRightOpen,
  PanelBottomClose,
  PanelBottomOpen,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";
import { useWorkspaceEngineStore } from "@/store/workspace-engine-store";
import { useEulaStore } from "@/store/eula-store";
import { useAuthStore } from "@/store/auth-store";
import { Button } from "@/components/ui/button";
import { Avatar } from "@/components/ui/avatar";

const APP_ITEMS = [
  { id: "trading" as const, label: "Trading", icon: LineChart, href: "/workspace/trading" },
  { id: "network" as const, label: "Network", icon: Network, href: "/workspace/network" },
  { id: "code" as const, label: "Code", icon: Code2, href: "/workspace/code" },
  { id: "security" as const, label: "Security", icon: Shield, href: "/workspace/security" },
  { id: "research" as const, label: "Research", icon: FlaskConical, href: "/workspace/research" },
];

export function WorkspaceHeader({
  onToggleRight,
  onToggleBottom,
}: {
  onToggleRight: () => void;
  onToggleBottom: () => void;
}) {
  const pathname = usePathname();
  const router = useRouter();
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const user = useAuthStore((s) => s.user);
  const logout = useAuthStore((s) => s.logout);
  const hasAccepted = useEulaStore((s) => s.hasAccepted);
  const activeApp = useWorkspaceEngineStore((s) => s.activeApp);
  const panel = useWorkspaceEngineStore((s) => s.panel);

  const handleLogout = async () => {
    await logout();
    router.push("/login");
  };

  return (
    <header className="flex h-12 shrink-0 items-center justify-between border-b border-[var(--color-border)] bg-[var(--color-bg-secondary)] px-4">
      <div className="flex items-center gap-3">
        <button
          onClick={() => router.push("/dashboard")}
          className="flex items-center gap-2 hover:opacity-80 transition-opacity"
        >
          <span className="text-lg">🧠</span>
          <span className="text-sm font-semibold">Enal AI OS</span>
        </button>
        <span className="text-xs text-[var(--color-text-secondary)]">/</span>
        <span className="text-xs text-[var(--color-text-secondary)] capitalize">{activeApp} Workspace</span>
      </div>

      <div className="flex items-center gap-1">
        <Button variant="ghost" size="sm" onClick={onToggleRight} title={panel.right.open ? "Close right panel" : "Open right panel"}>
          {panel.right.open ? <PanelRightClose className="h-4 w-4" /> : <PanelRightOpen className="h-4 w-4" />}
        </Button>
        <Button variant="ghost" size="sm" onClick={onToggleBottom} title={panel.bottom.open ? "Close bottom panel" : "Open bottom panel"}>
          {panel.bottom.open ? <PanelBottomClose className="h-4 w-4" /> : <PanelBottomOpen className="h-4 w-4" />}
        </Button>
        <div className="ml-2 flex items-center gap-2">
          <Avatar fallback={user?.username || "U"} size="sm" />
          <span className="text-xs text-[var(--color-text-secondary)]">{user?.username || "User"}</span>
          <Button variant="ghost" size="sm" onClick={handleLogout} className="text-[var(--color-text-secondary)] hover:text-[var(--color-danger)]">
            Sign out
          </Button>
        </div>
      </div>
    </header>
  );
}

