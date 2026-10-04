"use client";

import { useEffect, useState } from "react";
import { Activity, CheckCircle2, FileText, RefreshCw, ScrollText } from "lucide-react";
import { useConsoleStore } from "@/store/console-store";
import { relativeTime } from "@/lib/format";
import { cn } from "@/lib/utils";

export function ConsoleStatusBar() {
  const health = useConsoleStore((s) => s.health.data);
  const lastSyncAt = useConsoleStore((s) => s.lastSyncAt);
  const benchmarkRun = useConsoleStore((s) => s.benchmarkRun.data);
  const cceStatus = useConsoleStore((s) => s.cceStatus.data);
  const summary = useConsoleStore((s) => s.lifecycleSummary.data);
  const loadEnvironment = useConsoleStore((s) => s.loadEnvironment);
  const loadBenchmark = useConsoleStore((s) => s.loadBenchmark);
  const [now, setNow] = useState(() => Date.now());

  useEffect(() => {
    const timer = window.setInterval(() => setNow(Date.now()), 15000);
    return () => window.clearInterval(timer);
  }, []);

  const lastBenchmark =
    benchmarkRun?.summary.total ? (benchmarkRun.summary.passed ? "passed" : "no data") : null;
  const benchmarkAt = cceStatus?.timestamp ?? benchmarkRun?.suite_id ?? null;

  return (
    <footer className="flex h-9 shrink-0 items-center gap-4 border-t border-[var(--ecp-border)] bg-[var(--ecp-topbar)] px-4 text-[11px] text-[var(--ecp-text-muted)]">
      <StatusItem
        icon={
          health?.status === "ok" ? (
            <CheckCircle2 className="h-3.5 w-3.5 text-[var(--ecp-success)]" />
          ) : (
            <Activity className="h-3.5 w-3.5 text-[var(--ecp-alert)]" />
          )
        }
        label="API"
        value={health ? `${health.service} ${health.version}` : "checking"}
      />
      <Divider />
      <StatusItem
        icon={<ScrollText className="h-3.5 w-3.5 text-[var(--ecp-sky)]" />}
        label="Benchmark"
        value={
          benchmarkAt
            ? `${relativeTime(benchmarkAt, now)}${lastBenchmark ? ` · ${lastBenchmark}` : ""}`
            : "never run"
        }
      />
      <Divider />
      <StatusItem
        icon={<RefreshCw className="h-3.5 w-3.5 text-[var(--ecp-gov)]" />}
        label="Last sync"
        value={relativeTime(lastSyncAt, now)}
      />
      {summary && (
        <>
          <Divider />
          <StatusItem
            icon={<span className="h-1.5 w-1.5 rounded-full bg-[var(--ecp-gov)]" />}
            label="Packs"
            value={`${summary.loaded}/${summary.total} loaded`}
          />
        </>
      )}
      <div className="ml-auto flex items-center gap-3">
        <span className="hidden items-center gap-1.5 md:inline-flex">
          <FileText className="h-3.5 w-3.5 text-[var(--ecp-text-dim)]" />
          RFC-0055 · Pilar 4 Governance
        </span>
        <button
          type="button"
          onClick={() => {
            loadEnvironment();
            loadBenchmark();
          }}
          className={cn(
            "rounded-md border border-[var(--ecp-border)] px-2 py-0.5 transition-colors",
            "text-[var(--ecp-text-dim)] hover:border-[var(--ecp-gov)] hover:text-[var(--ecp-text)]"
          )}
        >
          Refresh
        </button>
      </div>
    </footer>
  );
}

function Divider() {
  return <span className="h-3 w-px bg-[var(--ecp-border)]" />;
}

function StatusItem({
  icon,
  label,
  value,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
}) {
  return (
    <span className="flex items-center gap-1.5 whitespace-nowrap">
      {icon}
      <span className="text-[var(--ecp-text-dim)]">{label}</span>
      <span className="text-[var(--ecp-text-muted)]">{value}</span>
    </span>
  );
}
