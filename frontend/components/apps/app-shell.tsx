"use client";

import { useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { ArrowLeft, Home } from "lucide-react";
import { useAuthStore } from "@/store/auth-store";
import { useEulaStore } from "@/store/eula-store";
import { useLauncherStore } from "@/store/launcher-store";
import type { CapabilityApp } from "./capability-registry";

interface AppShellProps {
  app: CapabilityApp;
  children: React.ReactNode;
}

export function AppShell({ app, children }: AppShellProps) {
  const router = useRouter();
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const hasAccepted = useEulaStore((s) => s.hasAccepted);
  const recordRecent = useLauncherStore((s) => s.recordRecent);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/login");
      return;
    }
    if (!hasAccepted()) {
      router.push("/eula");
      return;
    }
    recordRecent(app.id);
  }, [isAuthenticated, hasAccepted, router, app.id, recordRecent]);

  if (!isAuthenticated || !hasAccepted()) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[var(--color-bg-primary)]">
        <div className="animate-spin h-8 w-8 border-2 border-[var(--color-accent)] border-t-transparent rounded-full" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[var(--color-bg-primary)]">
      {/* App header */}
      <header className="flex items-center justify-between border-b border-[var(--color-border)] bg-[var(--color-bg-secondary)] px-4 py-3">
        <div className="flex items-center gap-3">
          <button
            onClick={() => router.push("/dashboard")}
            className="flex items-center gap-1.5 rounded-lg px-2 py-1.5 text-sm text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-tertiary)] hover:text-[var(--color-text-primary)] transition-colors"
          >
            <ArrowLeft className="h-4 w-4" />
            Back
          </button>
          <div className="flex items-center gap-2">
            <span className="text-2xl">{app.icon}</span>
            <div>
              <h1 className="text-sm font-semibold text-[var(--color-text-primary)]">
                {app.name}
              </h1>
              <p className="text-xs text-[var(--color-text-secondary)]">
                {app.description}
              </p>
            </div>
          </div>
        </div>
        <Link
          href="/dashboard"
          className="rounded-lg p-2 text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-tertiary)] hover:text-[var(--color-text-primary)] transition-colors"
          aria-label="Go to dashboard"
        >
          <Home className="h-4 w-4" />
        </Link>
      </header>

      {/* App content */}
      <main className="flex-1">{children}</main>
    </div>
  );
}
