"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { LockKeyhole, ShieldAlert } from "lucide-react";
import { ConsoleSidebar } from "./console-sidebar";
import { ConsoleSearch, EnvironmentStatus } from "./console-topbar";
import { ConsoleStatusBar } from "./console-status-bar";
import { useAuthStore } from "@/store/auth-store";
import { useConsoleStore } from "@/store/console-store";

export function ConsoleShell({ children }: { children: React.ReactNode }) {
  const [collapsed, setCollapsed] = useState(false);
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const isLoading = useAuthStore((s) => s.isLoading);
  const initialize = useAuthStore((s) => s.initialize);
  const loadEnvironment = useConsoleStore((s) => s.loadEnvironment);
  const loadGovernance = useConsoleStore((s) => s.loadGovernance);
  const loadBenchmark = useConsoleStore((s) => s.loadBenchmark);
  const loadMarketplace = useConsoleStore((s) => s.loadMarketplace);

  useEffect(() => {
    initialize();
  }, [initialize]);

  useEffect(() => {
    if (!isAuthenticated) return;
    loadEnvironment();
    loadGovernance();
    loadBenchmark();
    loadMarketplace();
  }, [
    isAuthenticated,
    loadEnvironment,
    loadGovernance,
    loadBenchmark,
    loadMarketplace,
  ]);

  return (
    <div className="ecp-console flex h-screen w-full overflow-hidden text-[var(--ecp-text)]">
      <ConsoleSidebar collapsed={collapsed} onToggle={() => setCollapsed((value) => !value)} />

      <div className="flex min-w-0 flex-1 flex-col">
        <header className="flex h-[60px] shrink-0 items-center gap-4 border-b border-[var(--ecp-border)] bg-[var(--ecp-topbar)] px-4">
          <ConsoleSearch />
          <EnvironmentStatus />
        </header>

        <main className="min-h-0 flex-1 overflow-y-auto px-5 py-5">
          {isAuthenticated ? children : <AuthGate loading={isLoading} />}
        </main>

        <ConsoleStatusBar />
      </div>
    </div>
  );
}

function AuthGate({ loading }: { loading: boolean }) {
  const router = useRouter();
  return (
    <div className="grid h-full place-items-center">
      <div className="w-full max-w-md rounded-xl border border-[var(--ecp-border)] bg-[var(--ecp-surface)] p-6 text-center">
        <div className="mx-auto mb-4 grid h-12 w-12 place-items-center rounded-xl bg-[var(--ecp-surface-3)]">
          {loading ? (
            <ShieldAlert className="h-5 w-5 text-[var(--ecp-alert)]" />
          ) : (
            <LockKeyhole className="h-5 w-5 text-[var(--ecp-gov)]" />
          )}
        </div>
        <h1 className="text-base font-semibold">
          {loading ? "Restoring session…" : "Authentication required"}
        </h1>
        <p className="mt-2 text-sm text-[var(--ecp-text-muted)]">
          The governance console reads live backend state. Sign in to continue.
        </p>
        <button
          type="button"
          onClick={() => router.push("/login")}
          className="mt-5 w-full rounded-lg bg-[var(--ecp-gov)] px-4 py-2.5 text-sm font-semibold text-[#04121a] transition-opacity hover:opacity-90"
        >
          Go to sign in
        </button>
      </div>
    </div>
  );
}