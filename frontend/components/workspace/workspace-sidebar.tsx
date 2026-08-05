"use client";

import { usePathname, useRouter } from "next/navigation";
import {
  LineChart,
  Network,
  Code2,
  Shield,
  FlaskConical,
} from "lucide-react";
import { useWorkspaceEngineStore } from "@/store/workspace-engine-store";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const APP_ITEMS = [
  { id: "trading" as const, label: "Trading", icon: LineChart, href: "/workspace/trading" },
  { id: "network" as const, label: "Network", icon: Network, href: "/workspace/network" },
  { id: "code" as const, label: "Code", icon: Code2, href: "/workspace/code" },
  { id: "security" as const, label: "Security", icon: Shield, href: "/workspace/security" },
  { id: "research" as const, label: "Research", icon: FlaskConical, href: "/workspace/research" },
];

export function WorkspaceSidebar({ activeApp }: { activeApp: string }) {
  const router = useRouter();
  const setActiveApp = useWorkspaceEngineStore((s) => s.setActiveApp);

  const handleClick = (id: string, href: string) => {
    setActiveApp(id as any);
    router.push(href);
  };

  return (
    <aside className="flex w-14 flex-col items-center border-r border-[var(--color-border)] bg-[var(--color-bg-secondary)] py-2 gap-1">
      {APP_ITEMS.map((item) => {
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
              "w-10 h-10",
              isActive
                ? "bg-[var(--color-accent)] text-white hover:bg-[var(--color-accent)] hover:text-white"
                : "text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)]"
            )}
          >
            <Icon className="h-4 w-4" />
          </Button>
        );
      })}
    </aside>
  );
}

