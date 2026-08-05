"use client";

import { useRouter } from "next/navigation";
import { useWorkspaceEngineStore } from "@/store/workspace-engine-store";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import {
  LineChart,
  Network,
  Code2,
  Shield,
  FlaskConical,
  LayoutDashboard,
} from "lucide-react";

const APPS = [
  { id: "trading" as const, label: "Trading", icon: LineChart, href: "/workspace/trading" },
  { id: "network" as const, label: "Network", icon: Network, href: "/workspace/network" },
  { id: "code" as const, label: "Code", icon: Code2, href: "/workspace/code" },
  { id: "security" as const, label: "Security", icon: Shield, href: "/workspace/security" },
  { id: "research" as const, label: "Research", icon: FlaskConical, href: "/workspace/research" },
];

export function WorkspaceDock() {
  const router = useRouter();
  const activeApp = useWorkspaceEngineStore((s) => s.activeApp);
  const setActiveApp = useWorkspaceEngineStore((s) => s.setActiveApp);

  const handleClick = (id: typeof APPS[number]["id"], href: string) => {
    setActiveApp(id);
    router.push(href);
  };

  return (
    <div className="flex items-center justify-center gap-1 border-t border-[var(--color-border)] bg-[var(--color-bg-secondary)] px-4 py-1.5">
      <Button
        variant="ghost"
        size="icon"
        onClick={() => router.push("/dashboard")}
        title="Dashboard"
        className="text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)]"
      >
        <LayoutDashboard className="h-4 w-4" />
      </Button>

      <div className="w-px h-5 bg-[var(--color-border)] mx-1" />

      {APPS.map((item) => {
        const Icon = item.icon;
        const isActive = activeApp === item.id;
        return (
          <Button
            key={item.id}
            variant="ghost"
            size="icon"
            onClick={() => handleClick(item.id, item.href)}
            title={item.label}
            className={cn(
              "h-8 w-8",
              isActive
                ? "bg-[var(--color-accent)] text-white hover:bg-[var(--color-accent)] hover:text-white"
                : "text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)]"
            )}
          >
            <Icon className="h-4 w-4" />
          </Button>
        );
      })}
    </div>
  );
}
