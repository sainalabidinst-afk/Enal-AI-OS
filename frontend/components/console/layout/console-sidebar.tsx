"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Activity,
  Boxes,
  Gauge,
  LayoutGrid,
  LogOut,
  Mic,
  Settings as SettingsIcon,
  ShoppingBag,
  SlidersHorizontal,
  Workflow,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { useAuthStore } from "@/store/auth-store";

interface NavEntry {
  href: string;
  label: string;
  icon: typeof Gauge;
  hint: string;
}

const PRIMARY_NAV: NavEntry[] = [
  { href: "/console", label: "Dashboard", icon: Gauge, hint: "Governance overview" },
  { href: "/console/packs", label: "Capability Packs", icon: Boxes, hint: "Registered packs" },
  { href: "/console/builder", label: "Builder", icon: Workflow, hint: "Agent / tool pipeline" },
  { href: "/console/evaluation", label: "Evaluation", icon: Activity, hint: "Scenario scoring" },
  { href: "/console/marketplace", label: "Marketplace", icon: ShoppingBag, hint: "Clone templates" },
  { href: "/console/voice", label: "Voice Agent", icon: Mic, hint: "Jenny persona" },
];

const SECONDARY_NAV: NavEntry[] = [
  { href: "/console/settings", label: "Settings", icon: SettingsIcon, hint: "Model & integrations" },
  { href: "/console/observability", label: "Observability", icon: LayoutGrid, hint: "Runtime telemetry" },
];

export function ConsoleSidebar({ collapsed, onToggle }: { collapsed: boolean; onToggle: () => void }) {
  const pathname = usePathname();
  const user = useAuthStore((s) => s.user);
  const logout = useAuthStore((s) => s.logout);

  const renderItem = (item: NavEntry) => {
    const active =
      item.href === "/console" ? pathname === "/console" : pathname.startsWith(item.href);
    const Icon = item.icon;
    return (
      <Link
        key={item.href}
        href={item.href}
        title={collapsed ? item.label : undefined}
        className={cn(
          "group flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm transition-colors",
          active
            ? "bg-[var(--ecp-surface-3)] text-[var(--ecp-text)] shadow-[inset_2px_0_0_var(--ecp-gov)]"
            : "text-[var(--ecp-text-muted)] hover:bg-[var(--ecp-surface-2)] hover:text-[var(--ecp-text)]"
        )}
      >
        <Icon
          className={cn(
            "h-4 w-4 shrink-0",
            active ? "text-[var(--ecp-gov)]" : "text-[var(--ecp-text-dim)] group-hover:text-[var(--ecp-text-muted)]"
          )}
        />
        {!collapsed && (
          <span className="flex-1 truncate">
            <span className="block truncate font-medium">{item.label}</span>
            <span className="block truncate text-[11px] text-[var(--ecp-text-dim)]">{item.hint}</span>
          </span>
        )}
      </Link>
    );
  };

  return (
    <aside
      className={cn(
        "flex h-full shrink-0 flex-col border-r border-[var(--ecp-border)] bg-[var(--ecp-sidebar)] transition-[width] duration-200",
        collapsed ? "w-[72px]" : "w-[248px]"
      )}
    >
      <div className="flex h-[60px] items-center gap-2.5 border-b border-[var(--ecp-border)] px-4">
        <div className="grid h-9 w-9 shrink-0 place-items-center rounded-lg bg-gradient-to-br from-[var(--ecp-gov)] to-[var(--ecp-sky)] text-[13px] font-black text-[#04121a]">
          EC
        </div>
        {!collapsed && (
          <div className="min-w-0">
            <p className="truncate text-sm font-bold tracking-tight">ECP</p>
            <p className="truncate text-[10px] uppercase tracking-[0.16em] text-[var(--ecp-text-dim)]">
              Cognitive Platform
            </p>
          </div>
        )}
      </div>

      <nav className="flex-1 space-y-1 overflow-y-auto p-3">
        {!collapsed && (
          <p className="px-3 pb-1 pt-2 text-[10px] font-semibold uppercase tracking-[0.18em] text-[var(--ecp-text-dim)]">
            Platform
          </p>
        )}
        {PRIMARY_NAV.map(renderItem)}
        {!collapsed && (
          <p className="px-3 pb-1 pt-4 text-[10px] font-semibold uppercase tracking-[0.18em] text-[var(--ecp-text-dim)]">
            System
          </p>
        )}
        {SECONDARY_NAV.map(renderItem)}
      </nav>

      <div className="space-y-2 border-t border-[var(--ecp-border)] p-3">
        <button
          type="button"
          onClick={onToggle}
          className="flex w-full items-center gap-2 rounded-lg px-3 py-2 text-xs text-[var(--ecp-text-dim)] transition-colors hover:bg-[var(--ecp-surface-2)] hover:text-[var(--ecp-text)]"
        >
          <SlidersHorizontal className="h-4 w-4" />
          {!collapsed && <span>Collapse rail</span>}
        </button>
        {!collapsed && (
          <div className="flex items-center gap-2 rounded-lg bg-[var(--ecp-surface)] px-3 py-2">
            <div className="grid h-7 w-7 shrink-0 place-items-center rounded-full bg-[var(--ecp-surface-3)] text-[11px] font-semibold text-[var(--ecp-gov)]">
              {(user?.username || "operator").slice(0, 2).toUpperCase()}
            </div>
            <span className="min-w-0 flex-1 truncate text-xs">{user?.username || "operator"}</span>
            <button
              type="button"
              onClick={logout}
              title="Sign out"
              className="text-[var(--ecp-text-dim)] transition-colors hover:text-[var(--ecp-danger)]"
            >
              <LogOut className="h-3.5 w-3.5" />
            </button>
          </div>
        )}
      </div>
    </aside>
  );
}