"use client";

import { useRouter } from "next/navigation";
import {
  ChevronDown,
  LineChart,
  Network,
  Code2,
  Shield,
  FlaskConical,
  Database,
  Brain,
  FolderOpen,
  FileText,
  BarChart3,
  Activity,
  LogOut,
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

const COGNITIVE_ITEMS = [
  { id: "cognitive" as const, label: "Cognitive", icon: Brain, href: "/workspace/cognitive" },
];

const ARTIFACT_ITEMS = [
  { label: "Documents", icon: FolderOpen, href: "/artifacts" },
  { label: "Reports", icon: FileText, href: "/artifacts/reports" },
  { label: "Benchmarks", icon: BarChart3, href: "/artifacts/benchmarks" },
];

const OBSERVABILITY_ITEMS = [
  { label: "Metrics", icon: BarChart3, href: "/metrics" },
  { label: "Logs", icon: Activity, href: "/observability/logs" },
  { label: "Trace", icon: LogOut, href: "/observability/trace" },
];

export function WorkspaceSidebar({ activeApp }: { activeApp: string }) {
  const router = useRouter();
  const sidebarCollapsed = useWorkspaceStore((s) => s.sidebarCollapsed);
  const toggleSidebar = useWorkspaceStore((s) => s.toggleSidebar);
  const workspaces = useWorkspaceStore((s) => s.workspaces);
  const activeWorkspace = useWorkspaceStore((s) => s.activeWorkspace);
  const setActiveWorkspace = useWorkspaceStore((s) => s.setActiveWorkspace);

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
          <div className="relative w-full">
            <select
              value={activeWorkspace}
              onChange={(e) => setActiveWorkspace(e.target.value)}
              className="appearance-none w-full rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] px-2 py-1 text-xs text-[var(--color-text-primary)] focus:border-[var(--color-accent)] focus:outline-none pr-6 cursor-pointer"
            >
              {workspaces.map((ws) => (
                <option key={ws.id} value={ws.id}>
                  {ws.name}
                </option>
              ))}
            </select>
            <ChevronDown
              className="absolute right-1 top-1/2 -translate-y-1/2 h-3 w-3 text-[var(--color-text-secondary)] pointer-events-none"
            />
          </div>
        )}
        <Button
          variant="ghost"
          size="icon"
          onClick={toggleSidebar}
          aria-label={sidebarCollapsed ? "Expand sidebar" : "Collapse sidebar"}
          className="h-6 w-6 shrink-0"
        >
          {sidebarCollapsed ? "▶" : "◀"}
        </Button>
      </div>

      <div className="flex-1 overflow-y-auto p-2">
        {!sidebarCollapsed && (
          <span className="text-[10px uppercase tracking-wide text-[var(--color-text-secondary)] mb-1">
            Apps
          </span>
        )}
        <SidebarGroup>
          {APP_ITEMS.map((item) => {
            const isActive = activeApp === item.id;
            return (
              <SidebarItem
                key={item.id}
                icon={<item.icon className="h-4 w-4" />}
                label={item.label}
                active={isActive}
                collapsed={sidebarCollapsed}
                onClick={() => handleClick(item.id, item.href)}
              />
            );
          })}
        </SidebarGroup>

        {!sidebarCollapsed && (
          <>
            <SidebarGroup label="Cognitive">
              {COGNITIVE_ITEMS.map((item) => {
                const isActive = activeApp === item.id;
                return (
                  <SidebarItem
                    key={item.id}
                    icon={<item.icon className="h-4 w-4" />}
                    label={item.label}
                    active={isActive}
                    collapsed={sidebarCollapsed}
                    onClick={() => handleClick(item.id, item.href)}
                  />
                );
              })}
            </SidebarGroup>

            <SidebarGroup label="Artifacts">
              {ARTIFACT_ITEMS.map((item) => (
                <SidebarItem
                  key={item.label}
                  icon={<item.icon className="h-4 w-4" />}
                  label={item.label}
                  collapsed={sidebarCollapsed}
                  onClick={() => handleClick(item.label, item.href)}
                />
              ))}
            </SidebarGroup>

            <SidebarGroup label="Observability">
              {OBSERVABILITY_ITEMS.map((item) => (
                <SidebarItem
                  key={item.label}
                  icon={<item.icon className="h-4 w-4" />}
                  label={item.label}
                  collapsed={sidebarCollapsed}
                  onClick={() => handleClick(item.label, item.href)}
                />
              ))}
            </SidebarGroup>
          </>
        )}
      </div>
    </aside>
  );
}
