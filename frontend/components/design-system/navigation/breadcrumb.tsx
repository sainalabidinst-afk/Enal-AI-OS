"use client";

import { usePathname } from "next/navigation";
import { ChevronRight, Home } from "lucide-react";
import { Button } from "@/components/ui/button";

const SEGMENT_MAP: Record<string, string> = {
  trading: "Trading Analyst",
  network: "Network Engineer",
  code: "Code Engineer",
  security: "Security Engineer",
  research: "Research Assistant",
  database: "Database Engineer",
  watchlist: "Watchlist",
  portfolio: "Portfolio",
  orders: "Orders",
  scanner: "Scanner",
  alerts: "Alerts",
  topology: "Topology",
  devices: "Devices",
  configurations: "Configurations",
  templates: "Templates",
  deployments: "Deployments",
  explorer: "Explorer",
  editor: "Editor",
  terminal: "Terminal",
  git: "Git",
  extensions: "Extensions",
  sql: "SQL Editor",
  schema: "Schema",
  results: "Results",
  history: "History",
  search: "Search",
  findings: "Findings",
  synthesis: "Synthesis",
  citations: "Citations",
  report: "Report",
};

export function Breadcrumb() {
  const pathname = usePathname();
  const segments = pathname.split("/").filter(Boolean);

  return (
    <nav aria-label="Breadcrumb" className="flex items-center gap-1 text-xs text-[var(--color-secondary-500)]">
      <Button
        variant="ghost"
        size="icon"
        onClick={() => (window.location.href = "/dashboard")}
        className="h-6 w-6"
        aria-label="Dashboard"
      >
        <Home className="h-3.5 w-3.5" />
      </Button>

      {segments.map((segment, index) => {
        const isLast = index === segments.length - 1;
        const label = SEGMENT_MAP[segment] || segment;

        return (
          <span key={segment} className="flex items-center gap-1">
            <ChevronRight className="h-3 w-3 opacity-60" aria-hidden="true" />
            {isLast ? (
              <span className="text-[var(--color-foreground)] font-medium">{label}</span>
            ) : (
              <span className="hover:text-[var(--color-foreground)] cursor-pointer">{label}</span>
            )}
          </span>
        );
      })}
    </nav>
  );
}
