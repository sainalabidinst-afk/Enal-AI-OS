"use client";

import { usePathname, useRouter } from "next/navigation";
import {
  LineChart,
  Network,
  Code2,
  Shield,
  FlaskConical,
  Database,
} from "lucide-react";
import { useWorkspaceStore } from "@/components/workspace/stores/workspace-store";
import { SidebarItem } from "@/components/workspace/sidebar/sidebar-item";
import { SidebarGroup } from "@/components/workspace/sidebar/sidebar-group";
import { Button } from "@/components/design-system/primitives/button";
import { cn } from "@/lib/utils";

const APP_ITEMS = [
  { id: "trading" as const, label: "Trading", icon: LineChart, href: "/workspace/trading" },
  { id: "network" as const, label: "Network", icon: Network, href: "/workspace/network" },
  { id: "code" as const, label: "Code", icon: Code2, href: "/workspace/code" },
  { id: "security" as const, label: "Security", icon: Shield, href: "/workspace/security" },
  { id: "research" as const, label: "Research", icon: FlaskConical, href: "/workspace/research" },
  { id: "database" as const, label: "Database", icon: Database, href: "/workspace/database" },
];

export function WorkspaceSidebar({ activeApp }: { activeApp: string }) {
  const router = useRouter();
  const sidebarCollapsed = useWorkspaceStore((s) => s.sidebarCollapsed);
  const toggleSidebar = useWorkspaceStore((s) => s.toggleSidebar);

  const handleClick = (id: string, href: string) => {
    router.push(href);
  };

  return (
    <aside
      className={cn(
        "flex flex-col border-r border-[var(--color-border)] bg-[var(--color-bg-secondary)] transition-all duration-200",
        sidebarCollapsed ? "w-14" : "w-56"
      )}
      aria-label="Workspace sidebar"
    >
      <div className="flex items-center justify-between p-2 border-b border-[var(--color-border)]">
        {!sidebarCollapsed && (
          <span className="text-xs font-medium text-[var(--color-text-secondary)] uppercase tracking-wide">
            Apps
          </span>
        )}
        <Button
          variant="ghost"
          size="icon"
          onClick={toggleSidebar}
          aria-label={sidebarCollapsed ? "Expand sidebar" : "Collapse sidebar"}
          className="h-6 w-6"
        >
          {sidebarCollapsed ? "▶" : "◀"}
        </Button>
      </div>

      <div className="flex-1 overflow-y-auto p-2">
      <SidebarGroup>
        {APP_ITEMS.map((item) => {
          const isActive = activeApp === item.id;
          return (
            <SidebarItem
              key={item.id}
              icon={<item.icon className="h-4 w-4" />}
              label={item.label}
              active={isActive}
              onClick={() => handleClick(item.id, item.href)}
            />
          );
        })}
      </SidebarGroup>
      </div>
    </aside>
  );
}
